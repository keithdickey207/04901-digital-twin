# 04901 Digital Twin — Spatial Matrix

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Godot](https://img.shields.io/badge/Godot-4.2-blue.svg)](https://godotengine.org/)

Godot-based sovereign digital twin for the Waterville, ME (04901) lattice.

Part of the **Aether / Sovereign** stack. Ingests neural spike telemetry from the
5D Loom pipeline and engraves vertices into a persistent point-cloud OBJ lattice.

## Components

| File | Role |
|------|------|
| `scripts/ram_ingest.gd` | Headless ingest: reads `/dev/shm/sovereign_spikes.json`, appends OBJ vertices |
| `scripts/telemetry_ingest.gd` | Spatial delta calculator for lattice origin vs signal vectors |
| `project.godot` | Godot 4.2 project config (`04901_Spatial_Matrix`) |
| `commons_pulse.gd` | Commons pulse visualization (legacy) |

## Waterville Lattice Origin

- **Lat (X):** 44.5520
- **Lon (Z):** -69.6317
- **Alt (Y):** spike count from phonon bridge

## Quick Start

```bash
git clone https://github.com/keithdickey207/04901-digital-twin.git
cd 04901-digital-twin

# One-shot telemetry ingest (requires spike JSON from phonon bridge)
godot --headless -s scripts/ram_ingest.gd

# Spatial delta demo
godot --headless -s scripts/telemetry_ingest.gd
```

## 5D Loom Pipeline

```
LEO/SDR intercept → phonon_bridge.py → /dev/shm/sovereign_spikes.json
                                              ↓
                                    ram_ingest.gd (this repo)
                                              ↓
                              user://04901_lattice.obj (point cloud)
```

See also:
- [aether/sovereign/daemons](https://github.com/keithdickey207/aether/tree/main/sovereign/daemons) — phonon bridge + loom heartbeat
- [04901-sentinel](https://github.com/keithdickey207/04901-sentinel) — LEO tracking + RTL-SDR handoff
- [04901-alchemical-chamber](https://github.com/keithdickey207/04901-alchemical-chamber) — Newton's lab node

## License

MIT License — Copyright (c) 2026 Keith Dickey. See [LICENSE](LICENSE).
