# 04901 Digital Twin — Spatial Matrix

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Godot](https://img.shields.io/badge/Godot-4.2-blue.svg)](https://godotengine.org/)

Godot-based sovereign digital twin for the Waterville, ME (04901) lattice.

**Anchor:** `44.5520°N, 69.6317°W` (Waterville, ME 04901)

Part of the **WQSH / Dickey.OS** sovereign stack. Ingests neural spike telemetry from the 5D Loom pipeline and engraves vertices into a persistent point-cloud OBJ lattice — the Godot 3D counterpart to [District 04901 Grid](https://github.com/keithdickey207/District_04901_Grid) (React 2D C2) and [waterville-ar](https://github.com/keithdickey207/waterville-ar) (building footprints).

## Components

| File | Role |
|------|------|
| `scripts/ram_ingest.gd` | Headless ingest: reads `/dev/shm/sovereign_spikes.json`, appends OBJ vertices |
| `scripts/telemetry_ingest.gd` | Spatial delta calculator for lattice origin vs signal vectors |
| `project.godot` | Godot 4.2 project config (`04901_Spatial_Matrix`) |
| `commons_pulse.gd` | Commons pulse visualization (legacy) |
| `control.tscn` / `node_3d.tscn` | Scene stubs for 3D lattice viewer |

## Waterville Lattice Origin

| Axis | Value |
|------|-------|
| **Lat (X)** | 44.5520 |
| **Lon (Z)** | -69.6317 |
| **Alt (Y)** | spike count from phonon bridge |

Same anchor as District 04901 Grid, chronosat, and dickey-sovereign-core telemetry mesh.

## Quick Start

```bash
git clone https://github.com/keithdickey207/04901-digital-twin.git
cd 04901-digital-twin

# One-shot telemetry ingest (requires spike JSON from phonon bridge)
godot --headless -s scripts/ram_ingest.gd

# Spatial delta demo
godot --headless -s scripts/telemetry_ingest.gd

# Open in Godot editor
godot --path .
```

> **Penguin / ChromeOS:** Install Godot 4.2+ locally; do not commit the binary. Pair with Tailscale for `/dev/shm` spike feeds from homelab nodes.

## Architecture

```
LEO/SDR intercept → phonon_bridge.py → /dev/shm/sovereign_spikes.json
                                              │
                                              ▼
                                    ram_ingest.gd (this repo)
                                              │
                                              ▼
                              user://04901_lattice.obj (point cloud)
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    ▼                         ▼                         ▼
            Aether Godot bridge      waterville-ar buildings    District 04901 Grid
            (Navigation station)     (CityBuilder.gd 3D)        (React VM 2D C2)
```

### Parallel telemetry paths

| Path | Protocol | Consumer |
|------|----------|----------|
| 5D Loom / phonon | `/dev/shm/sovereign_spikes.json` | `ram_ingest.gd` (this repo) |
| Mesh devices | UDP `:2368` JSON | [District 04901 Grid](https://github.com/keithdickey207/District_04901_Grid) |
| Fusion / tactile | UDP via sovereign-core | React VM FusionHUD / TactileHUD |
| Orbital | JSON from chronosat daemon | Godot chronosat_viewer |

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

## Sovereign Stack

| Project | Role |
|---------|------|
| **[Aether Core](https://github.com/keithdickey207/aether)** | Brain hub — USD-4 protocol, RF lab, medical, Godot 4 bridge |
| **[District 04901 Grid](https://github.com/keithdickey207/District_04901_Grid)** | Spatial C2 — React VM canvas, UDP/WS telemetry mesh |
| **[dickey-sovereign-core](https://github.com/keithdickey207/dickey-sovereign-core)** | Fusion + tactile physics + LogisticsMatrix |
| **[waterville-ar](https://github.com/keithdickey207/waterville-ar)** | Godot city builder — 78 building footprints |
| **04901-digital-twin** (this repo) | Godot 3D spatial matrix — spike lattice OBJ |
| **[04901-alchemical-chamber](https://github.com/keithdickey207/04901-alchemical-chamber)** | Godot Newton chymical lab node |
| **[chronosat](https://github.com/keithdickey207/chronosat)** | Orbital daemon + historical Landsat viewer |
| **[04901-sentinel](https://github.com/keithdickey207/04901-sentinel)** | NORAD tracker + bug bounty hunter |
| **[04901_Taxi_Dispatch](https://github.com/keithdickey207/04901_Taxi_Dispatch)** | Local-first taxi dispatch + fleet sim |
| **[document-fraud-detection-engine](https://github.com/keithdickey207/document-fraud-detection-engine)** | Sovereign document forensics |
| **[secure-self-healing-orchestrator](https://github.com/keithdickey207/secure-self-healing-orchestrator)** | Zero-trust LLM self-repair + FBI OSINT |
| **[newtons-alchemical-lab](https://github.com/keithdickey207/newtons-alchemical-lab)** | Historical chymistry CLI explorer |
| **[sovereign-sync](https://github.com/keithdickey207/sovereign-sync)** | Mesh glue — Syncthing, Tailscale, worktrees |
| **[dotfiles](https://github.com/keithdickey207/dotfiles)** | Multi-device bootstrap shell + env |
| **[goodperson](https://github.com/keithdickey207/goodperson)** | Good Person Protocol — daily practice CLI |

Sync mesh: Tailscale + Syncthing + git worktrees — see `~/SOVEREIGN_SYNC_QUICKSTART.md` and [sovereign-sync](https://github.com/keithdickey207/sovereign-sync).


## License

MIT License — Copyright (c) 2026 Keith Dickey. See [LICENSE](LICENSE).