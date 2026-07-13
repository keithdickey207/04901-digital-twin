#!/usr/bin/env python3
"""
God Mode multi-spectrum defensive COP ingest for 04901 Spatial Matrix.
Custom sovereign engine — no third-party game runtimes.

Keith Alan Dickey — WSDS / 04901 Studio · DEFENSIVE ONLY
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spatial_matrix import GOD_MODE_OBJ, SHM_GOD, ingest_god_mode  # noqa: E402


def main() -> int:
    print("\n[+] 04901 GOD MODE: Metaverse paint ingest online")
    print("[*] Doctrine: DEFENSIVE ONLY — military / fire / rescue protection")
    print("[*] Engine: sovereign-spatial-matrix (custom Python)")

    out = ingest_god_mode()
    if not out.get("ok"):
        print(f"[-] {out.get('reason', 'ingest failed')}")
        print("    Run: bash ~/projects/sovereign-engine/start-earth.sh --daemon")
        print("    Then: WS god_mode_enter or open /quest-god-mode.html")
        return 1

    print(
        f"[GOD] active={out.get('active')} | {out.get('building')} | "
        f"persona={out.get('persona')}"
    )
    s = out.get("summary") or {}
    print(
        f"[GOD] life H={s.get('humans', 0)} A={s.get('animals', 0)} | "
        f"threats={s.get('total_threats', 0)} | drones={s.get('drones', 0)} "
        f"missiles={s.get('missiles', 0)} chem={s.get('chemical', 0)} "
        f"cyber={s.get('cyber', 0)}"
    )
    print(
        f"[!] Engraved {out.get('life', 0)} life + {out.get('threats', 0)} "
        f"threat vertices → {GOD_MODE_OBJ}"
    )
    playbook = out.get("playbook") or []
    if playbook:
        print("[PLAYBOOK]")
        for i, line in enumerate(playbook, 1):
            print(f"  {i}. {line}")
    if out.get("defcon") is not None:
        print(f"[DEFENSE] DEFCON {out.get('defcon')} threat={out.get('threat_level')}")
    print("[*] God Mode ingest complete. Lattice ready for custom engine viewport.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
