#!/usr/bin/env python3
"""Spatial delta calculator for lattice origin vs signal vectors."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spatial_matrix import telemetry_demo  # noqa: E402


def main() -> int:
    print("\n[+] 04901 SPATIAL MATRIX: Headless Engine Online")
    print("[*] Processing spatial vectors...")
    d = telemetry_demo()
    print("[!] Telemetry Mapped.")
    print(
        f"    -> Origin Node: ({d['origin_lat']}, {d['origin_alt']}, {d['origin_lon']})"
    )
    print(
        f"    -> Signal Node: ({d['signal_lat']}, {d['signal_alt']}, {d['signal_lon']})"
    )
    print(f"    -> 3D Spatial Delta (Distance): {d['spatial_delta']}")
    print("\n[*] Matrix calculations complete. Shutting down spatial core.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
