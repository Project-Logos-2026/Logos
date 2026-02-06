
import { Component, signal, computed, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './app.component.html',
  styles: [`
    :host {
      display: block;
    }
    .logo-container {
      transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 1.5s ease-in-out;
    }
    .faded-out {
      opacity: 0.15;
      transform: scale(0.65) translateY(-140px);
    }
    .message-container {
      mask-image: linear-gradient(to bottom, transparent, black 15%, black 85%, transparent);
    }
    @keyframes mic-pulse {
      0%, 100% { filter: drop-shadow(0 0 2px rgba(34, 211, 238, 0.5)); transform: scale(1); }
      50% { filter: drop-shadow(0 0 12px rgba(34, 211, 238, 0.8)); transform: scale(1.1); }
    }
    .mic-active {
      animation: mic-pulse 1.5s ease-in-out infinite;
      color: #22d3ee !important;
    }
  `]
})
export class AppComponent {
  private apiService = inject(ApiService);
  
  messages = signal<Message[]>([]);
  inputText = signal('');
  isProcessing = signal(false);
  isListening = signal(false);
  
  hasStartedInteraction = computed(() => this.messages().length > 0);

  private recognition: any;

  constructor() {
    this.initSpeechRecognition();
  }

  private initSpeechRecognition() {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = 'en-US';

      this.recognition.onstart = () => {
        this.isListening.set(true);
      };

      this.recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        this.inputText.set(transcript);
        this.isListening.set(false);
      };

      this.recognition.onerror = () => {
        this.isListening.set(false);
      };

      this.recognition.onend = () => {
        this.isListening.set(false);
      };
    }
  }

  toggleVoiceInput() {
    if (!this.recognition) {
      console.warn('Speech recognition not supported in this browser.');
      return;
    }

    if (this.isListening()) {
      this.recognition.stop();
    } else {
      this.recognition.start();
    }
  }

  async sendMessage() {
    const text = this.inputText().trim();
    if (!text || this.isProcessing()) return;

    const userMsg: Message = {
      role: 'user',
      content: text,
      timestamp: new Date()
    };

    this.messages.update(msgs => [...msgs, userMsg]);
    this.inputText.set('');
    this.isProcessing.set(true);
    this.scrollToBottom();

    try {
      const response = await this.apiService.generateResponse(text);
      const assistantMsg: Message = {
        role: 'assistant',
        content: response,
        timestamp: new Date()
      };
      this.messages.update(msgs => [...msgs, assistantMsg]);
    } catch (err) {
      console.error('Core disconnect:', err);
      const errorMsg: Message = {
        role: 'assistant',
        content: "ERR_PROTOCOL_BREACH: Failed to synchronize with LOGOS core. Re-establishing link...",
        timestamp: new Date()
      };
      this.messages.update(msgs => [...msgs, errorMsg]);
    } finally {
      this.isProcessing.set(false);
      this.scrollToBottom();
    }
  }

  scrollToBottom() {
    setTimeout(() => {
      const el = document.getElementById('chat-scroll-area');
      if (el) {
        el.scrollTo({
          top: el.scrollHeight,
          behavior: 'smooth'
        });
      }
    }, 150);
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }
}
