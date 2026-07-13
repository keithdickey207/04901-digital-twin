#!/usr/bin/env python3
"""Headless phonon spike → lattice OBJ engrave (sovereign spatial matrix)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spatial_matrix import DEFAULT_LATTICE_OBJ, ingest_spikes  # noqa: E402


def main() -> int:
    print("\n[+] 04901 SPATIAL MATRIX: Persistent Point-Cloud Generator Online")
    vertex = ingest_spikes()
    if not vertex:
        print("[-] No neural spike data found in /dev/shm.")
        return 1
    print(f"[!] Neural Telemetry Engraved to Lattice -> {vertex}")
    print(f"[*] Point-cloud geometry updated → {DEFAULT_LATTICE_OBJ}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
