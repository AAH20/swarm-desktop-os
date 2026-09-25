"""
Telemetry Stream Router for Swarm-Desktop-OS.
Projects token-bounded, role-specific sub-contexts to each agent seat.
"""

from typing import Dict, Any, List
from .models import SwarmOSState, SwarmRole, AgentSeat


class TelemetryStreamRouter:
    """Routes lean, targeted desktop state slices to each specialized agent model."""

    @staticmethod
    def get_seat_view(state: SwarmOSState, seat_id: str) -> Dict[str, Any]:
        """Builds an optimized, role-bounded context payload for an agent seat."""
        seat = state.seats.get(seat_id)
        if not seat:
            return {"error": "Seat not found"}

        payload: Dict[str, Any] = {
            "session_id": state.session_id,
            "seat_id": seat.seat_id,
            "role": seat.role.value,
            "model": seat.model_name,
            "assigned_window": seat.assigned_window_id,
            "fencing_token": seat.fencing_token,
        }

        # Role-based context projection:
        if seat.role == SwarmRole.SUPERVISOR:
            # Claude Opus 5.5 receives high-level executive fleet overview
            payload["overview"] = {
                "active_seats": [s.seat_id for s in state.seats.values() if s.is_active],
                "windows": {
                    w_id: {
                        "title": w.title,
                        "assigned_to": w.assigned_seat_id,
                        "active": w.is_active,
                        "last_line": w.content_lines[-1] if w.content_lines else ""
                    }
                    for w_id, w in state.windows.items()
                },
                "security_status": "NORMAL" if not any(a.threat_detected for a in state.audit_history) else "ALERT"
            }

        elif seat.role == SwarmRole.GUI_OPERATOR:
            # GPT-6 Astra receives targeted UI elements of browser
            win = state.windows.get(seat.assigned_window_id or "window_browser")
            if win:
                payload["window_ui"] = {
                    "title": win.title,
                    "url": win.input_text,
                    "interactive_elements": [l for l in win.content_lines if "Button" in l or "input" in l],
                    "status": "Ready for click/input"
                }

        elif seat.role == SwarmRole.CLI_OPERATOR:
            # DeepSeek V4.1-Flash receives shell history and prompt
            win = state.windows.get(seat.assigned_window_id or "window_terminal")
            if win:
                payload["terminal"] = {
                    "last_lines": win.content_lines[-5:],
                    "cwd": "/workspace",
                    "status": "Ready for command execution"
                }

        elif seat.role == SwarmRole.SECURITY_SENTINEL:
            # Gemini 3.8 Flash Cyber receives cross-window event stream for anomaly detection
            payload["audit_stream"] = {
                "inspected_windows": list(state.windows.keys()),
                "total_audits": len(state.audit_history),
                "threats_blocked": sum(1 for a in state.audit_history if a.threat_detected)
            }

        return payload
