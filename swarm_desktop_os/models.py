"""
Data models for Swarm-Desktop-OS multi-agent virtual desktop multiplexer.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import time


class SwarmRole(str, Enum):
    SUPERVISOR = "supervisor"              # Claude Opus 5.5 (Mission Commander)
    GUI_OPERATOR = "gui_operator"          # GPT-6 Astra (Browser & GUI Forms)
    CLI_OPERATOR = "cli_operator"          # DeepSeek V4.1-Flash (High-throughput Terminal)
    SECURITY_SENTINEL = "security_sentinel"# Gemini 3.8 Flash Cyber (Out-of-band visual audit)
    OBSERVER = "observer"


@dataclass
class AgentSeat:
    seat_id: str
    agent_id: str
    role: SwarmRole
    model_name: str
    assigned_window_id: Optional[str] = None
    fencing_token: int = 0
    is_active: bool = True
    last_heartbeat: float = field(default_factory=time.time)


@dataclass
class WindowTile:
    window_id: str
    title: str
    rect: Tuple[int, int, int, int]  # (x, y, w, h)
    assigned_seat_id: Optional[str] = None
    is_active: bool = False
    content_lines: List[str] = field(default_factory=list)
    input_text: str = ""


@dataclass
class SeatAction:
    seat_id: str
    action_type: str  # "click", "type", "command", "audit"
    target_window_id: str
    payload: Dict[str, Any]
    fencing_token: int


@dataclass
class ActionResult:
    success: bool
    seat_id: str
    target_window_id: str
    fencing_token: int
    message: str
    output_data: Optional[Dict[str, Any]] = None


@dataclass
class SecurityAuditVerdict:
    is_safe: bool
    threat_detected: bool = False
    threat_type: Optional[str] = None
    confidence: float = 1.0
    details: str = "Clean"
    quarantine_triggered: bool = False


@dataclass
class SwarmOSState:
    session_id: str
    seats: Dict[str, AgentSeat] = field(default_factory=dict)
    windows: Dict[str, WindowTile] = field(default_factory=dict)
    global_epoch: int = 1
    audit_history: List[SecurityAuditVerdict] = field(default_factory=list)
