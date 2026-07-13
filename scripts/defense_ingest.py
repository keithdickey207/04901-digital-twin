#!/usr/bin/env python3
"""Sovereign Defense Layer — spatial twin ingest (custom engine)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spatial_matrix import DEFAULT_LATTICE_OBJ, SHM_DEFENSE, ingest_defense  # noqa: E402


def main() -> int:
    print("\n[+] 04901 DEFENSE LAYER: Spatial Matrix Defense Ingest")
    if not SHM_DEFENSE.is_file():
        print("[-] No defense posture on bus. Run district_bridge first.")
    result = ingest_defense()
    if result.get("defense"):
        print(
            f"[DEFENSE] DEFCON {result.get('defcon')} | "
            f"Threat: {result.get('threat')} | "
            f"{result.get('layers', 0)} active layers"
        )
        print(f"[!] Defense posture engraved to lattice → {DEFAULT_LATTICE_OBJ}")
    if result.get("spikes"):
        print(f"[*] Phonon spike merged: {result.get('spike_vertex')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
