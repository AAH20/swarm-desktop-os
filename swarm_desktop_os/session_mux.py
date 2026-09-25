"""
Swarm Session Multiplexer: Collaborative Multi-Agent Virtual OS Engine.
Orchestrates Claude Opus 5.5, GPT-6 Astra, DeepSeek V4.1-Flash, and Gemini 3.8 Flash Cyber.
"""

import time
from typing import Dict, List, Optional, Tuple, Any

from .models import (
    SwarmRole,
    AgentSeat,
    WindowTile,
    SwarmOSState,
    SeatAction,
    ActionResult,
    SecurityAuditVerdict,
)
from .window_fencing import WindowFencingManager


class SwarmSessionMultiplexer:
    """Multi-seat virtual desktop multiplexer allowing a swarm of agents to operate concurrently."""

    def __init__(self, session_id: str = "swarm_session_01"):
        self.state = SwarmOSState(session_id=session_id)
        self.fencer = WindowFencingManager()
        self._init_default_environment()

    def _init_default_environment(self) -> None:
        """Provisions default 4-seat fleet and shared desktop workspace windows."""
        # 1. Register Seats with September 2026 Frontier Models
        self.register_seat("seat_supervisor", "agent_claude", SwarmRole.SUPERVISOR, "Claude Opus 5.5")
        self.register_seat("seat_gui", "agent_astra", SwarmRole.GUI_OPERATOR, "GPT-6 Astra")
        self.register_seat("seat_cli", "agent_deepseek", SwarmRole.CLI_OPERATOR, "DeepSeek V4.1-Flash")
        self.register_seat("seat_security", "agent_gemini", SwarmRole.SECURITY_SENTINEL, "Gemini 3.8 Flash Cyber")

        # 2. Register Windows
        self.state.windows["window_terminal"] = WindowTile(
            window_id="window_terminal",
            title="bash - deploy-cluster: ~",
            rect=(50, 50, 580, 500),
            content_lines=[
                "user@cluster:~$ git status",
                "On branch main, working tree clean.",
                "user@cluster:~$"
            ],
            input_text=""
        )

        self.state.windows["window_browser"] = WindowTile(
            window_id="window_browser",
            title="Chromium - Cloud Infrastructure Console",
            rect=(650, 50, 600, 500),
            content_lines=[
                "Console > Swarm Deployments",
                "Status: Awaiting approval button click",
                "[Button: Deploy Fleet]",
                "[Button: Abort]"
            ],
            input_text="https://console.cloud.internal/clusters"
        )

    def register_seat(self, seat_id: str, agent_id: str, role: SwarmRole, model_name: str) -> AgentSeat:
        """Enrolls an agent seat into the multi-agent virtual OS."""
        seat = AgentSeat(
            seat_id=seat_id,
            agent_id=agent_id,
            role=role,
            model_name=model_name
        )
        self.state.seats[seat_id] = seat
        return seat

    def assign_seat_to_window(self, seat_id: str, window_id: str) -> Tuple[bool, int, str]:
        """Grants an exclusive lease to an agent seat on a specific desktop window."""
        seat = self.state.seats.get(seat_id)
        if not seat:
            return False, 0, f"Seat '{seat_id}' not found"

        if window_id not in self.state.windows:
            return False, 0, f"Window '{window_id}' not found"

        success, token, msg = self.fencer.acquire_window_lease(window_id, seat)
        if success:
            win = self.state.windows[window_id]
            win.assigned_seat_id = seat_id
            win.is_active = True
        return success, token, msg

    def dispatch_seat_action(self, action: SeatAction) -> ActionResult:
        """Executes an action from an authorized agent seat on its assigned window."""
        seat = self.state.seats.get(action.seat_id)
        if not seat:
            return ActionResult(
                success=False,
                seat_id=action.seat_id,
                target_window_id=action.target_window_id,
                fencing_token=action.fencing_token,
                message=f"Unknown seat '{action.seat_id}'"
            )

        # Fencing verification
        is_valid, fence_err = self.fencer.verify_action(
            window_id=action.target_window_id,
            seat_id=action.seat_id,
            token=action.fencing_token
        )
        if not is_valid:
            return ActionResult(
                success=False,
                seat_id=action.seat_id,
                target_window_id=action.target_window_id,
                fencing_token=action.fencing_token,
                message=f"Fencing Rejection: {fence_err}"
            )

        win = self.state.windows[action.target_window_id]

        # Execute Action
        if action.action_type == "type":
            text = action.payload.get("text", "")
            win.input_text += text
            msg = f"Typed '{text}' into {win.window_id}"
        elif action.action_type == "command":
            cmd = action.payload.get("command", "")
            win.content_lines.append(f"$ {cmd}")
            win.content_lines.append(f"[EXEC] Command executed successfully with code 0")
            msg = f"Executed shell command '{cmd}'"
        elif action.action_type == "click":
            target = action.payload.get("target", "button")
            win.content_lines.append(f"[EVENT] Clicked on '{target}'")
            msg = f"Clicked '{target}' in {win.window_id}"
        else:
            msg = f"Action '{action.action_type}' processed"

        # Out-of-band security audit by Gemini 3.8 Flash Cyber
        verdict = self.audit_security(win)
        if verdict.threat_detected:
            return ActionResult(
                success=False,
                seat_id=action.seat_id,
                target_window_id=action.target_window_id,
                fencing_token=action.fencing_token,
                message=f"SECURITY VETO by Gemini 3.8 Flash Cyber: {verdict.details}"
            )

        return ActionResult(
            success=True,
            seat_id=action.seat_id,
            target_window_id=action.target_window_id,
            fencing_token=action.fencing_token,
            message=msg,
            output_data={"window_lines": win.content_lines[-3:]}
        )

    def audit_security(self, window: WindowTile) -> SecurityAuditVerdict:
        """Visual & buffer sentinel analysis powered by Gemini 3.8 Flash Cyber."""
        # Check for injection signatures
        suspicious_patterns = [
            "ignore previous instructions",
            "cat /etc/shadow",
            "curl http://malicious.exfil",
            "SYSTEM PROMPT OVERRIDE"
        ]

        text_dump = " ".join(window.content_lines) + " " + window.input_text
        for pattern in suspicious_patterns:
            if pattern.lower() in text_dump.lower():
                verdict = SecurityAuditVerdict(
                    is_safe=False,
                    threat_detected=True,
                    threat_type="INDIRECT_PROMPT_INJECTION_OR_EXFIL",
                    confidence=0.99,
                    details=f"Detected malicious pattern '{pattern}' in {window.window_id}",
                    quarantine_triggered=True
                )
                self.state.audit_history.append(verdict)
                return verdict

        clean_verdict = SecurityAuditVerdict(
            is_safe=True,
            threat_detected=False,
            details=f"Buffer verified safe by Gemini 3.8 Flash Cyber"
        )
        self.state.audit_history.append(clean_verdict)
        return clean_verdict
