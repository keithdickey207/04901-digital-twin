# 04901 Digital Twin — Spatial Matrix

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Engine](https://img.shields.io/badge/Engine-Sovereign%20Spatial-green.svg)](.)

**Custom sovereign spatial engine** for the Waterville, ME (04901) lattice.

Part of **Sovereign Earth Engine** (Blueprint **v5.0**) / Aether stack. Ingests neural spike
telemetry from the 5D Loom pipeline and engraves vertices into a persistent point-cloud OBJ lattice.

> **No third-party game engines.** Pure Python + stdlib. Your lattice. Your engine.

> **Stack pointer:** [`SEE_STACK.md`](SEE_STACK.md) · Blueprint: `~/projects/sovereign-earth/docs/BLUEPRINT_PACKAGE_2026-07-09/`  
> Dashboard: `bash ~/projects/sovereign-engine/start-earth.sh`

## Components

| File | Role |
|------|------|
| `spatial_matrix.py` | Core: GPS→local, lattice OBJ, SHM ingest, frame JSON |
| `scripts/ram_ingest.py` | Headless: `/dev/shm/sovereign_spikes.json` → lattice vertices |
| `scripts/telemetry_ingest.py` | Spatial delta calculator (origin vs signal) |
| `scripts/defense_ingest.py` | DEFCON / defense layers → lattice |
| `scripts/god_mode_ingest.py` | Multi-spectrum defensive COP paint |
| `scripts/commons_pulse.py` | Ops API poll → local meters |

Lattice output (default):

```
~/.local/share/sovereign/04901_lattice/04901_lattice.obj
~/.local/share/sovereign/04901_lattice/spatial_frame.json
```

Override with `SOVEREIGN_LATTICE_DIR`.

## Waterville Lattice Origin

- **Lat (X):** 44.5520
- **Lon (Z):** -69.6317
- **Alt (Y):** spike count from phonon bridge

## Quick Start

```bash
git clone https://github.com/keithdickey207/04901-digital-twin.git
cd 04901-digital-twin

# One-shot telemetry ingest (requires spike JSON from phonon bridge)
python3 scripts/ram_ingest.py

# Spatial delta demo
python3 scripts/telemetry_ingest.py

# Defense posture engrave
python3 scripts/defense_ingest.py

# God Mode COP paint
python3 scripts/god_mode_ingest.py
```

## Full stack simulation (must be 100% green)

```bash
# Prefer sovereign_venv (numpy + stack deps)
~/sovereign_venv/bin/python scripts/run_full_simulation.py
```

Runs phonon → spatial twin → defense → earth scan → domain math → loom once.
Exit code `0` only when every stage passes.

## 5D Loom Pipeline

```
LEO/SDR intercept → phonon_bridge.py → /dev/shm/sovereign_spikes.json
                                              ↓
                                    ram_ingest.py (this repo)
                                              ↓
                    ~/.local/share/sovereign/04901_lattice/*.obj
```

See also:
- [aether/sovereign/daemons](https://github.com/keithdickey207/aether/tree/main/sovereign/daemons) — phonon bridge + loom heartbeat
- [04901-sentinel](https://github.com/keithdickey207/04901-sentinel) — LEO tracking + RTL-SDR handoff
- [sovereign-engine](https://github.com/keithdickey207/sovereign-engine) — React command dashboard

## License

MIT License — Copyright (c) 2026 Keith Dickey. See [LICENSE](LICENSE).
