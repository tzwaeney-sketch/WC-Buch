#!/usr/bin/env python3
"""Validate all 12 production STL files."""
import trimesh
import numpy as np
import json
import os
import sys

READY = "/home/user/WC-Buch/modular_strala_lamp/READY_TO_PRINT"
PARTS = [
    "01_Fuss_Rund.stl",
    "02_Fuss_Design.stl",
    "03_Koerper_Kugel.stl",
    "04_Koerper_Abgeflachte_Kugel.stl",
    "05_Koerper_Organisch.stl",
    "06_Koerper_Geometrisch.stl",
    "07_Koerper_Schmal_Ring.stl",
    "08_Koerper_Schmal_Gerippt.stl",
    "09_Schirm_Klassisch.stl",
    "10_Schirm_Gerippt.stl",
    "11_Schirm_Organisch.stl",
    "12_STRALA_Fassungsbefestigung.stl",
]

BAMBU_P2S_BUILD = (256, 256, 256)  # mm

results = []
all_pass = True

for fname in PARTS:
    fpath = os.path.join(READY, fname)
    r = {"file": fname, "status": "FAIL"}

    if not os.path.exists(fpath):
        r["error"] = "FILE NOT FOUND"
        results.append(r); all_pass = False; continue

    size = os.path.getsize(fpath)
    r["file_size_bytes"] = size
    if size < 1000:
        r["error"] = f"FILE TOO SMALL: {size} bytes"
        results.append(r); all_pass = False; continue

    try:
        mesh = trimesh.load(fpath, force='mesh')
        bb = mesh.bounding_box.extents
        vol = float(mesh.volume)
        r["face_count"] = len(mesh.faces)
        r["vertex_count"] = len(mesh.vertices)
        r["bounding_box_mm"] = [round(float(b), 2) for b in bb]
        r["volume_mm3"] = round(vol, 1)
        r["volume_cm3"] = round(vol / 1000, 2)
        r["mass_pla_g"] = round(vol / 1000 * 1.24, 1)
        r["mass_petg_g"] = round(vol / 1000 * 1.27, 1)
        r["is_watertight"] = bool(mesh.is_watertight)
        r["is_volume"] = bool(mesh.is_volume)
        fits_p2s = all(bb[i] <= BAMBU_P2S_BUILD[i] for i in range(3))
        r["fits_bambu_p2s"] = bool(fits_p2s)
        try:
            comps = mesh.split(only_watertight=False)
            r["component_count"] = len(comps)
        except Exception:
            r["component_count"] = None
        areas = mesh.area_faces
        r["degenerate_faces"] = int(np.sum(areas < 1e-10))
        r["min_dimension_mm"] = round(float(min(bb)), 2)
        bb_vol = bb[0]*bb[1]*bb[2]
        fill = vol/bb_vol if bb_vol > 0 else 1.0
        r["fill_ratio"] = round(fill, 3)
        r["estimated_hollow"] = bool(fill < 0.7)

        if not fits_p2s:
            r["error"] = f"EXCEEDS P2S BUILD VOLUME: {[round(b,1) for b in bb]}"
            all_pass = False
        elif not mesh.is_watertight:
            r["warning"] = "NOT WATERTIGHT - may need repair"
            r["status"] = "WARNING"
        else:
            r["status"] = "PASS"
    except Exception as e:
        r["error"] = str(e); all_pass = False

    results.append(r)
    print(f"[{r.get('status','FAIL'):7s}] {fname:40s} BB={str(r.get('bounding_box_mm','N/A')):28s} wt={r.get('is_watertight',False)} comp={r.get('component_count','?')}")

out_path = "/home/user/WC-Buch/modular_strala_lamp/exports/reports/production_validation.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump({"parts": results, "all_pass": all_pass}, f, indent=2)
print(f"\nAll pass: {all_pass}\nResults: {out_path}")
sys.exit(0 if all_pass else 1)
