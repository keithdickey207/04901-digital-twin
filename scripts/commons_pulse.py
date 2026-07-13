#!/usr/bin/env python3
"""Commons pulse — poll local ops API and map assets into local spatial meters."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spatial_matrix import commons_pulse_once  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description="04901 commons pulse spatial poller")
    p.add_argument(
        "--url",
        default="http://127.0.0.1:8000/api/operations/status",
        help="Local ops status API",
    )
    p.add_argument("--loop", action="store_true", help="Poll every 5s")
    p.add_argument("--interval", type=float, default=5.0)
    args = p.parse_args()

    print("[*] 04901 commons pulse — sovereign spatial matrix")
    if not args.loop:
        commons_pulse_once(args.url)
        return 0
    try:
        while True:
            print("[*] Polling local operational API...")
            commons_pulse_once(args.url)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Pulse stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
