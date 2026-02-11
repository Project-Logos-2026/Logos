"""
Event emission interface for GUI and telemetry subscribers.
"""


class EventEmitter:
    def emit(self, event_type: str, payload: dict) -> None:
        # Placeholder - integrate with existing event/logging system
        pass
