from pathlib import Path

from opentrons.simulate import simulate


def test_protocol_simulates_without_error():
    protocol_path = Path(__file__).parents[1] / "protocol.py"
    with protocol_path.open(encoding="utf-8") as protocol_file:
        run_log, bundle = simulate(protocol_file)

    commands = [entry["payload"]["text"] for entry in run_log]
    assert bundle is None
    assert any("Protocol complete" in command for command in commands)
    assert sum("Picking up tip" in command for command in commands) >= 50
