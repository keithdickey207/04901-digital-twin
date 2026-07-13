#!/usr/bin/env python3
"""
04901 + Sovereign stack — full local simulation harness.

Runs phonon → spatial lattice → defense/god-mode → earth scan → domain math.
Exits 0 only when every required stage passes. No third-party game engines.

Usage:
  python3 scripts/run_full_simulation.py
  LOOM_ONCE=1 bash ...  (also used by aether loom)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

HOME = Path.home()
TWIN = Path(__file__).resolve().parents[1]
EARTH = HOME / "projects" / "sovereign-earth"
AETHER = HOME / "projects" / "aether"
DEFENSE = HOME / "projects" / "sovereign-defense"
LATTICE_DIR = Path(
    os.environ.get(
        "SOVEREIGN_LATTICE_DIR",
        str(HOME / ".local" / "share" / "sovereign" / "04901_lattice"),
    )
)

PY = sys.executable
RESULTS: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    flag = "PASS" if ok else "FAIL"
    print(f"  [{flag}] {name}" + (f" — {detail}" if detail else ""))


def run_py(script: Path, env: dict | None = None, timeout: int = 120) -> tuple[bool, str]:
    if not script.is_file():
        return False, f"missing {script}"
    try:
        cp = subprocess.run(
            [PY, str(script)],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env or os.environ.copy(),
            cwd=str(script.parent if script.name != "phonon_bridge.py" else script.parent),
        )
        out = (cp.stdout or "") + (cp.stderr or "")
        return cp.returncode == 0, out.strip()[-500:]
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as exc:
        return False, str(exc)


def write_mock_buses() -> None:
    """Ensure defense + god-mode SHM exist for ingest paths."""
    spikes = {
        "x_lat": 44.5520,
        "y_alt_spikes": 42,
        "z_lon": -69.6317,
        "timestamp": str(int(time.time())),
        "engine": "sim-harness",
    }
    Path("/dev/shm/sovereign_spikes.json").write_text(json.dumps(spikes), encoding="utf-8")

    defense = {
        "defcon": 4,
        "threat_level": "GUARDED",
        "humans": 12,
        "animals": 3,
        "layers": [
            {"label": "SIGINT", "active": True, "quality": 0.8},
            {"label": "SPATIAL", "active": True, "quality": 0.9},
            {"label": "AIR", "active": True, "quality": 0.5},
            {"label": "CYBER", "active": False, "quality": 0.2},
            {"label": "CHEM", "active": True, "quality": 0.4},
            {"label": "LEO", "active": True, "quality": 0.7},
            {"label": "GROUND", "active": True, "quality": 0.6},
        ],
        "ts": time.time(),
    }
    Path("/dev/shm/sovereign_defense.json").write_text(json.dumps(defense), encoding="utf-8")

    god = {
        "active": True,
        "building_id": "home_16_kelsey",
        "building_name": "16 Kelsey",
        "persona": "joint",
        "persona_label": "Joint COP",
        "projection": "exterior",
        "threat_summary": {
            "humans": 4,
            "animals": 1,
            "total_threats": 2,
            "drones": 1,
            "missiles": 0,
            "chemical": 0,
            "cyber": 1,
        },
        "entities": [
            {
                "entity_class": "human",
                "lat": 44.5521,
                "lon": -69.6316,
                "alt_m": 2.0,
                "confidence": 0.9,
            },
            {
                "entity_class": "drone",
                "lat": 44.5530,
                "lon": -69.6300,
                "alt_m": 40.0,
                "confidence": 0.7,
            },
            {
                "entity_class": "animal",
                "lat": 44.5515,
                "lon": -69.6320,
                "alt_m": 0.0,
                "confidence": 0.6,
            },
        ],
        "sources": [
            {"id": "wifi_2.4", "power": 0.8},
            {"id": "bt_ble", "power": 0.4},
            {"id": "leo_uhf", "power": 0.55},
        ],
        "defensive_playbook": [
            "Harden perimeter RF",
            "Track drone vector",
            "Shelter non-combatants",
        ],
    }
    Path("/dev/shm/sovereign_god_mode.json").write_text(json.dumps(god), encoding="utf-8")


def stage_phonon() -> None:
    script = AETHER / "sovereign" / "daemons" / "phonon_bridge.py"
    ok, detail = run_py(script, timeout=90)
    spikes = Path("/dev/shm/sovereign_spikes.json")
    if spikes.is_file():
        data = json.loads(spikes.read_text())
        ok = ok and "y_alt_spikes" in data
        detail = f"spikes={data.get('y_alt_spikes')} mode={data.get('mode', '?')}"
    record("phonon_bridge → SHM spikes", ok, detail)


def stage_twin() -> None:
    sys.path.insert(0, str(TWIN))
    from spatial_matrix import (  # type: ignore
        DEFAULT_LATTICE_OBJ,
        GOD_MODE_OBJ,
        ingest_defense,
        ingest_god_mode,
        ingest_spikes,
        telemetry_demo,
    )

    demo = telemetry_demo()
    record(
        "spatial telemetry_demo",
        demo["spatial_delta"] > 0,
        f"delta={demo['spatial_delta']:.6f}",
    )

    v = ingest_spikes()
    record("ram_ingest (spikes→OBJ)", v is not None, str(v))

    d = ingest_defense()
    record(
        "defense_ingest",
        bool(d.get("defense")),
        f"DEFCON={d.get('defcon')} layers={d.get('layers')}",
    )

    g = ingest_god_mode()
    record(
        "god_mode_ingest",
        bool(g.get("ok")) and int(g.get("vertices", 0)) > 0,
        f"verts={g.get('vertices')} life={g.get('life')} threats={g.get('threats')}",
    )

    record("lattice OBJ exists", DEFAULT_LATTICE_OBJ.is_file(), str(DEFAULT_LATTICE_OBJ))
    record("god_mode OBJ exists", GOD_MODE_OBJ.is_file(), str(GOD_MODE_OBJ))

    # CLI scripts
    for name in (
        "telemetry_ingest.py",
        "ram_ingest.py",
        "defense_ingest.py",
        "god_mode_ingest.py",
    ):
        ok, detail = run_py(TWIN / "scripts" / name)
        record(f"cli {name}", ok, detail.splitlines()[-1] if detail else "")


def stage_earth() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [
            str(EARTH),
            str(HOME / "projects" / "district_04901_grid"),
            str(DEFENSE),
            env.get("PYTHONPATH", ""),
        ]
    )
    try:
        sys.path.insert(0, str(EARTH))
        sys.path.insert(0, str(HOME / "projects" / "district_04901_grid"))
        from earth_core import EarthEngine  # type: ignore

        eng = EarthEngine()
        scan = eng.ws_scan(44.5520, -69.6317)
        ok = scan.get("type") == "earth_scan"
        eng.publish_bus({"type": "sim_harness", "ts": time.time(), "scan_ok": ok})
        shm = Path("/dev/shm/sovereign_earth.json")
        record(
            "earth_core scan 04901",
            ok,
            f"keys={len(scan)} shm={shm.is_file()}",
        )
    except Exception as exc:
        record("earth_core scan 04901", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()

    ok, detail = run_py(EARTH / "scripts" / "verify_domain_math.py", env=env)
    record("domain math verify", ok, detail.splitlines()[-1] if detail else "")

    ok, detail = run_py(EARTH / "scripts" / "simulations.py", env=env)
    record("simulations.py orchestrator", ok, detail.splitlines()[-1] if detail else "")

    ok, detail = run_py(EARTH / "scripts" / "run_orchestrator.py", env=env)
    record("run_orchestrator", ok, detail.splitlines()[-1] if detail else "")


def stage_defense() -> None:
    try:
        sys.path.insert(0, str(DEFENSE))
        from defense_core import SovereignDefenseCore  # type: ignore

        core = SovereignDefenseCore()
        core.ingest_sigint(0.55, source="sim_harness")
        core.ingest_spatial(spike_count=42, lattice_ok=True)
        core.ingest_isr(humans=5, animals=2, tracks=7, motion=0.4)
        core.ingest_nav(gns_active=True, gnss_nodes=3)
        payload = core.publish_bus()
        shm = Path("/dev/shm/sovereign_defense.json")
        ok = isinstance(payload, dict) and shm.is_file()
        detail = (
            f"DEFCON={payload.get('defcon', payload.get('defcon_level', '?'))} "
            f"keys={len(payload)} shm={shm.is_file()}"
        )
        record("sovereign_defense_core", ok, detail)
    except Exception as exc:
        record("sovereign_defense_core", False, f"{type(exc).__name__}: {exc}")
        traceback.print_exc()


def stage_rf_paint() -> None:
    """One-shot UDP packet into spatial viewer logic (no long serve)."""
    try:
        sys.path.insert(0, str(AETHER / "rf_paint" / "spatial"))
        from rf_paint_viewer import RFPaintViewer  # type: ignore

        viewer = RFPaintViewer(LATTICE_DIR.parent / "rf_paint_sim", port=0)
        viewer.handle(
            {
                "type": "frequency_measurement",
                "measured_freq_hz": 2.412e9,
                "peak_power_dbm": -40.0,
                "timestamp": time.time(),
            }
        )
        viewer.handle(
            {
                "type": "accelerator_state",
                "mean_energy_mev": 12.5,
                "phase_deg": -15.0,
                "particles": [{"energy": 10.0, "phase": 1.0}],
            }
        )
        ok = viewer.obj_path.is_file() and viewer.packet_count == 2
        record("rf_paint spatial viewer", ok, f"packets={viewer.packet_count}")
    except Exception as exc:
        record("rf_paint spatial viewer", False, str(exc))


def stage_aether_bridge_import() -> None:
    script = AETHER / "dashboard" / "aether_bridge" / "bridge_server.py"
    try:
        import ast

        ast.parse(script.read_text(encoding="utf-8"))
        record("aether bridge_server parse", True, str(script))
    except Exception as exc:
        record("aether bridge_server parse", False, str(exc))


def stage_engine_purity() -> None:
    """Hard assert: no third-party game-engine project files remain in stack repos."""
    roots = [
        HOME / "projects" / "04901-digital-twin",
        HOME / "projects" / "aether",
        HOME / "projects" / "sovereign-earth",
        HOME / "projects" / "sovereign-engine",
        HOME / "projects" / "sovereign",
    ]
    bad: list[str] = []
    for root in roots:
        if not root.is_dir():
            continue
        for pat in ("*.gd", "*.tscn", "project.godot"):
            for p in root.rglob(pat):
                if ".git" in p.parts:
                    continue
                bad.append(str(p))
    record("engine purity (no third-party game assets)", len(bad) == 0, f"found={len(bad)}")


def main() -> int:
    print("=" * 60)
    print("SOVEREIGN FULL SIMULATION HARNESS")
    print(f"python: {PY}")
    print(f"twin:   {TWIN}")
    print("=" * 60)

    write_mock_buses()

    print("\n── 0. purity ──")
    stage_engine_purity()

    print("\n── 1. phonon ──")
    stage_phonon()

    print("\n── 2. spatial twin ──")
    # re-seed god mode after phonon may not touch it
    write_mock_buses()
    stage_twin()

    print("\n── 3. earth ──")
    stage_earth()

    print("\n── 4. defense ──")
    stage_defense()

    print("\n── 5. aether surfaces ──")
    stage_aether_bridge_import()
    stage_rf_paint()

    print("\n── 6. loom once ──")
    loom = AETHER / "sovereign" / "daemons" / "loom_heartbeat.sh"
    if loom.is_file():
        env = os.environ.copy()
        env["LOOM_ONCE"] = "1"
        try:
            cp = subprocess.run(
                ["bash", str(loom)],
                capture_output=True,
                text=True,
                timeout=90,
                env=env,
            )
            ok = cp.returncode == 0 and Path("/dev/shm/sovereign_spikes.json").is_file()
            record("loom_heartbeat LOOM_ONCE", ok, (cp.stdout + cp.stderr)[-300:])
        except Exception as exc:
            record("loom_heartbeat LOOM_ONCE", False, str(exc))
    else:
        record("loom_heartbeat LOOM_ONCE", False, "missing script")

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print("\n" + "=" * 60)
    print(f"RESULT: {passed}/{total} passed")
    if passed < total:
        print("FAILURES:")
        for name, ok, detail in RESULTS:
            if not ok:
                print(f"  - {name}: {detail}")
    else:
        print("100% — all simulation stages green.")
    print("=" * 60)
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
