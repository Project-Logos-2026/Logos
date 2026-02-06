
import { Injectable } from '@angular/core';
import { GoogleGenAI } from "@google/genai";

declare var process: any;

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // Fix: Replaced HttpClient with GoogleGenAI to fix "Property 'post' does not exist on type 'unknown'"
  // The API key is sourced from the environment as per instructions.
  private ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

  /**
   * Generates a response from the Gemini model.
   * Uses 'gemini-2.5-flash' for optimal performance and quality.
   */
  async generateResponse(text: string): Promise<string> {
    try {
      const result = await this.ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: [{ role: 'user', parts: [{ text }] }],
        config: {
          temperature: 0.7,
          topP: 0.95,
          topK: 40,
        }
      });

      return result.text;
    } catch (error) {
      console.error('Gemini Service Error:', error);
      throw new Error('Failed to synchronize with generative core.');
    }
  }
}
