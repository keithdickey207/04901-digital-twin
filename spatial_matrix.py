#!/usr/bin/env python3
"""
04901 Spatial Matrix — Sovereign Digital Twin core

Custom local spatial engine for the Waterville (04901) lattice.
No third-party game engines. Pure Python + stdlib.

Keith Alan Dickey — WSDS / 04901 Studio · MIT
"""

from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

# Waterville lattice origin
ORIGIN_LAT = 44.5520
ORIGIN_LON = -69.6317
ORIGIN_ALT = 0.0
METERS_PER_DEG_LAT = 111_320.0

DEFAULT_LATTICE_DIR = Path(os.environ.get(
    "SOVEREIGN_LATTICE_DIR",
    str(Path.home() / ".local" / "share" / "sovereign" / "04901_lattice"),
))
DEFAULT_LATTICE_OBJ = DEFAULT_LATTICE_DIR / "04901_lattice.obj"
GOD_MODE_OBJ = DEFAULT_LATTICE_DIR / "04901_god_mode_lattice.obj"
FRAME_JSON = DEFAULT_LATTICE_DIR / "spatial_frame.json"

SHM_SPIKES = Path("/dev/shm/sovereign_spikes.json")
SHM_DEFENSE = Path("/dev/shm/sovereign_defense.json")
SHM_GOD = Path("/dev/shm/sovereign_god_mode.json")


@dataclass
class Vec3:
    x: float
    y: float
    z: float

    def distance_to(self, other: "Vec3") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)


def meters_per_deg_lon(lat: float = ORIGIN_LAT) -> float:
    return METERS_PER_DEG_LAT * math.cos(math.radians(lat))


def gps_to_local(lat: float, lon: float, alt: float = 0.0) -> Vec3:
    """Map WGS84 to local ENU-ish meters relative to Waterville origin."""
    m_lon = meters_per_deg_lon(ORIGIN_LAT)
    x = (lon - ORIGIN_LON) * m_lon
    z = (lat - ORIGIN_LAT) * METERS_PER_DEG_LAT
    return Vec3(x, alt, z)


def local_to_gps(x: float, y: float, z: float) -> tuple[float, float, float]:
    m_lon = meters_per_deg_lon(ORIGIN_LAT)
    lon = ORIGIN_LON + x / m_lon
    lat = ORIGIN_LAT + z / METERS_PER_DEG_LAT
    return lat, lon, y


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def ensure_lattice_dir(path: Path = DEFAULT_LATTICE_DIR) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def append_vertices(
    obj_path: Path,
    vertices: Iterable[tuple[float, float, float, str]],
    header: str | None = None,
) -> int:
    """Append OBJ vertices (x y z + optional # comment). Returns count written."""
    ensure_lattice_dir(obj_path.parent)
    lines: list[str] = []
    count = 0
    for x, y, z, comment in vertices:
        if comment:
            lines.append(f"v {x:.6f} {y:.6f} {z:.6f} # {comment}\n")
        else:
            lines.append(f"v {x:.6f} {y:.6f} {z:.6f}\n")
        count += 1
    if not lines:
        return 0
    mode = "a" if obj_path.is_file() else "w"
    with obj_path.open(mode, encoding="utf-8") as f:
        if mode == "w":
            f.write(header or "# 04901 Sovereign Spatial Lattice — custom engine\n")
        f.writelines(lines)
    return count


def write_vertices_fresh(
    obj_path: Path,
    vertices: Iterable[tuple[float, float, float, str]],
    header: str,
    objects: dict[str, list[tuple[float, float, float, str]]] | None = None,
) -> int:
    """Overwrite OBJ with full lattice snapshot."""
    ensure_lattice_dir(obj_path.parent)
    count = 0
    with obj_path.open("w", encoding="utf-8") as f:
        f.write(header if header.endswith("\n") else header + "\n")
        if objects:
            for name, verts in objects.items():
                f.write(f"o {name}\n")
                for x, y, z, comment in verts:
                    if comment:
                        f.write(f"v {x:.6f} {y:.6f} {z:.6f} # {comment}\n")
                    else:
                        f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
                    count += 1
        else:
            for x, y, z, comment in vertices:
                if comment:
                    f.write(f"v {x:.6f} {y:.6f} {z:.6f} # {comment}\n")
                else:
                    f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
                count += 1
    return count


def write_frame_json(payload: dict[str, Any], path: Path = FRAME_JSON) -> None:
    ensure_lattice_dir(path.parent)
    payload = {**payload, "engine": "sovereign-spatial-matrix", "ts": time.time()}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def ingest_spikes(obj_path: Path = DEFAULT_LATTICE_OBJ) -> str | None:
    data = read_json(SHM_SPIKES)
    if not data:
        return None
    x = float(data.get("x_lat", ORIGIN_LAT))
    y = float(data.get("y_alt_spikes", 0.0))
    z = float(data.get("z_lon", ORIGIN_LON))
    n = append_vertices(
        obj_path,
        [(x, y, z, "phonon_spike")],
        header="# 04901 5D Loom Point Cloud Lattice — sovereign spatial matrix\n",
    )
    if n:
        msg = f"v {x} {y} {z}"
        write_frame_json({"last_spike": data, "vertex": msg, "lattice": str(obj_path)})
        return msg
    return None


def ingest_defense(obj_path: Path = DEFAULT_LATTICE_OBJ) -> dict[str, Any]:
    result: dict[str, Any] = {"defense": False, "spikes": False, "layers": 0}
    data = read_json(SHM_DEFENSE)
    verts: list[tuple[float, float, float, str]] = []
    if data:
        defcon = int(data.get("defcon", 5))
        threat = str(data.get("threat_level", "LOW"))
        y_defense = float(6 - defcon)
        verts.append((ORIGIN_LAT, y_defense, ORIGIN_LON, f"DEFCON{defcon} {threat}"))
        layer_idx = 0
        for layer in data.get("layers", []) or []:
            if not layer.get("active", False):
                continue
            offset = float(layer_idx) * 0.0001
            verts.append((
                ORIGIN_LAT + offset,
                float(layer.get("quality", 0.0)) * 5.0,
                ORIGIN_LON + offset,
                str(layer.get("label", "LAYER")),
            ))
            layer_idx += 1
        result["defense"] = True
        result["layers"] = layer_idx
        result["defcon"] = defcon
        result["threat"] = threat
        append_vertices(
            obj_path,
            verts,
            header="# 04901 Defense Lattice — Sovereign Spatial Matrix\n",
        )
    spike = ingest_spikes(obj_path)
    result["spikes"] = spike is not None
    result["spike_vertex"] = spike
    write_frame_json({"defense_ingest": result, "lattice": str(obj_path)})
    return result


def ingest_god_mode(obj_path: Path = GOD_MODE_OBJ) -> dict[str, Any]:
    data = read_json(SHM_GOD)
    if not data:
        return {"ok": False, "reason": f"no state at {SHM_GOD}"}

    entities = data.get("entities", []) or []
    sources = data.get("sources", []) or []
    summary = data.get("threat_summary", {}) or {}
    playbook = data.get("defensive_playbook", []) or []

    life: list[tuple[float, float, float, str]] = []
    threats: list[tuple[float, float, float, str]] = []
    spectrum: list[tuple[float, float, float, str]] = []

    for e in entities:
        lat = float(e.get("lat", ORIGIN_LAT))
        lon = float(e.get("lon", ORIGIN_LON))
        alt = float(e.get("alt_m", 0.0))
        local = gps_to_local(lat, lon, alt)
        cls = str(e.get("entity_class", "unknown"))
        conf = e.get("confidence", 0)
        vert = (local.x, local.y, local.z, f"{cls} conf={conf}")
        if cls in ("human", "animal"):
            life.append(vert)
        else:
            threats.append(vert)

    for si, s in enumerate(sources):
        power = float(s.get("power", 0.5))
        angle = si * 0.5
        r = 5.0 + power * 20.0
        spectrum.append((
            math.cos(angle) * r,
            power * 10.0,
            math.sin(angle) * r,
            f"spectrum {s.get('id', 'band')}",
        ))

    building = str(data.get("building_name", data.get("building_id", "AOI")))
    persona = str(data.get("persona_label", data.get("persona", "joint")))
    header = (
        f"# 04901 God Mode Lattice — multi-spectrum defensive paint\n"
        f"# building {building} persona {persona}\n"
        f"# engine sovereign-spatial-matrix\n"
    )
    n = write_vertices_fresh(
        obj_path,
        [],
        header=header,
        objects={
            "god_mode_life": life,
            "god_mode_threat": threats,
            "god_mode_spectrum": spectrum,
        },
    )
    out = {
        "ok": True,
        "active": data.get("active", False),
        "building": building,
        "persona": persona,
        "life": len(life),
        "threats": len(threats),
        "spectrum": len(spectrum),
        "vertices": n,
        "summary": summary,
        "playbook": playbook[:8],
        "lattice": str(obj_path),
    }
    defense = read_json(SHM_DEFENSE)
    if defense:
        out["defcon"] = defense.get("defcon")
        out["threat_level"] = defense.get("threat_level")
    write_frame_json({"god_mode": out})
    return out


def telemetry_demo() -> dict[str, float]:
    origin = Vec3(ORIGIN_LAT, 0.0, ORIGIN_LON)
    signal = Vec3(44.5550, 150.0, -69.6300)
    delta = origin.distance_to(signal)
    return {
        "origin_lat": origin.x,
        "origin_alt": origin.y,
        "origin_lon": origin.z,
        "signal_lat": signal.x,
        "signal_alt": signal.y,
        "signal_lon": signal.z,
        "spatial_delta": delta,
    }


def commons_pulse_once(api_url: str = "http://127.0.0.1:8000/api/operations/status") -> list[dict]:
    """Poll local ops API and map assets into local meters (stdlib only)."""
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(api_url, timeout=3) as resp:
            body = resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"[-] API unreachable: {exc}")
        return []

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        print(f"[-] JSON parse error: {exc}")
        return []

    updates = []
    for asset in payload.get("assets", []) or []:
        coords = str(asset.get("geo_coordinates", "0,0")).split(",")
        try:
            lat = float(coords[0])
            lon = float(coords[1])
        except (ValueError, IndexError):
            continue
        local = gps_to_local(lat, lon)
        updates.append({
            "asset_id": asset.get("asset_id"),
            "status": asset.get("asset_status"),
            "lat": lat,
            "lon": lon,
            "x": local.x,
            "y": local.y,
            "z": local.z,
        })
        print(
            f"[+] Kinetic Update: {asset.get('asset_id')} | "
            f"{asset.get('asset_status')} | {lat}, {lon} → "
            f"({local.x:.1f}, {local.y:.1f}, {local.z:.1f}) m"
        )
    if updates:
        write_frame_json({"commons_pulse": updates})
    return updates


if __name__ == "__main__":
    print("[*] 04901 Spatial Matrix core ready")
    print(f"    lattice dir: {DEFAULT_LATTICE_DIR}")
    print(f"    origin: {ORIGIN_LAT}, {ORIGIN_LON}")
    demo = telemetry_demo()
    print(f"    demo spatial delta: {demo['spatial_delta']:.6f}")
