"""
Window Fencing & Monotonic Token Manager for Swarm-Desktop-OS.
Prevents concurrent keystroke clashes and zombie subagent overwrite collisions.
"""

import time
from typing import Dict, Optional, Tuple
from .models import AgentSeat, ActionResult


class WindowFencingManager:
    """Controls window ownership, lease TTLs, and monotonically increasing fencing tokens."""

    def __init__(self, default_ttl_sec: float = 15.0):
        self.default_ttl = default_ttl_sec
        # window_id -> (seat_id, fencing_token, expiration_time)
        self.window_leases: Dict[str, Tuple[str, int, float]] = {}
        self.monotonic_counter: int = 100

    def acquire_window_lease(self, window_id: str, seat: AgentSeat) -> Tuple[bool, int, str]:
        """Grants exclusive input focus on a window with an incremented fencing token."""
        now = time.time()
        existing = self.window_leases.get(window_id)

        if existing:
            holder_seat_id, token, expires_at = existing
            if holder_seat_id == seat.seat_id:
                # Renew existing lease
                self.monotonic_counter += 1
                new_token = self.monotonic_counter
                self.window_leases[window_id] = (seat.seat_id, new_token, now + self.default_ttl)
                seat.fencing_token = new_token
                return True, new_token, "Lease renewed"

            if now < expires_at:
                # Active lease held by another agent seat
                return False, token, f"Window locked by seat '{holder_seat_id}' until {expires_at - now:.1f}s"

        # Grant fresh lease
        self.monotonic_counter += 1
        new_token = self.monotonic_counter
        self.window_leases[window_id] = (seat.seat_id, new_token, now + self.default_ttl)
        seat.fencing_token = new_token
        seat.assigned_window_id = window_id
        return True, new_token, f"Lease granted to {seat.seat_id} (Token #{new_token})"

    def verify_action(self, window_id: str, seat_id: str, token: int) -> Tuple[bool, str]:
        """Validates that incoming action has active lease and strictly valid monotonic fencing token."""
        now = time.time()
        existing = self.window_leases.get(window_id)

        if not existing:
            return False, f"No active lease for window '{window_id}'"

        holder_seat_id, active_token, expires_at = existing

        if holder_seat_id != seat_id:
            return False, f"Seat '{seat_id}' is not the authorized leaseholder of '{window_id}' (Held by '{holder_seat_id}')"

        if now > expires_at:
            return False, f"Lease expired for seat '{seat_id}' on window '{window_id}'"

        if token < active_token:
            return False, f"Stale fencing token #{token} rejected (Current active token #{active_token})"

        return True, "Valid"

    def release_lease(self, window_id: str, seat_id: str) -> bool:
        """Releases window lease immediately."""
        existing = self.window_leases.get(window_id)
        if existing and existing[0] == seat_id:
            del self.window_leases[window_id]
            return True
        return False
