"""
Swarm-Desktop-OS: Multi-Agent Collaborative Virtual OS Multiplexer for Swarm Computer-Use.
Orchestrates Claude Opus 5.5, GPT-6 Astra, DeepSeek V4.1-Flash, and Gemini 3.8 Flash Cyber across shared desktop sessions.
"""

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
from .session_mux import SwarmSessionMultiplexer
from .telemetry_stream import TelemetryStreamRouter

__version__ = "1.0.0"
__all__ = [
    "SwarmRole",
    "AgentSeat",
    "WindowTile",
    "SwarmOSState",
    "SeatAction",
    "ActionResult",
    "SecurityAuditVerdict",
    "WindowFencingManager",
    "SwarmSessionMultiplexer",
    "TelemetryStreamRouter",
]
