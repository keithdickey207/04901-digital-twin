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
| **[Aether Core](https://github.com/keithdickey207/aether)** | Brain hub — USD-4 protocol, Godot 4 bridge + map tiles |
| **04901-digital-twin** (this repo) | Godot 3D spatial matrix — spike lattice OBJ |
| **[District 04901 Grid](https://github.com/keithdickey207/District_04901_Grid)** | Spatial C2 — React VM canvas, UDP/WS telemetry |
| **[waterville-ar](https://github.com/keithdickey207/waterville-ar)** | Godot city builder — 78 building footprints |
| **[dickey-sovereign-core](https://github.com/keithdickey207/dickey-sovereign-core)** | Fusion + tactile physics streams |
| **[chronosat](https://github.com/keithdickey207/chronosat)** | Historical Landsat + live orbital daemon |
| **[dotfiles](https://github.com/keithdickey207/dotfiles)** | Multi-device environment bootstrap |

Sync: Tailscale + Syncthing + git worktrees — `~/SOVEREIGN_SYNC_QUICKSTART.md`

## Related Projects

- [aether](https://github.com/keithdickey207/aether) — Spaceship OS brain hub + Godot bridge
- [District_04901_Grid](https://github.com/keithdickey207/District_04901_Grid) — React spatial C2 / VM engine
- [waterville-ar](https://github.com/keithdickey207/waterville-ar) — Geospatial city builder
- [chronosat](https://github.com/keithdickey207/chronosat) — Orbital + historical Landsat layer

## License

MIT License — Copyright (c) 2026 Keith Dickey / Waterville Software Development Services. See [LICENSE](LICENSE).
