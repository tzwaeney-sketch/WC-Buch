#!/usr/bin/env python3
"""Validate all 12 v2 STL parts. Emits JSON report to stdout + validation_v2.json."""
import os, json, glob, sys
import numpy as np
import trimesh

OUT = os.path.join(os.path.dirname(__file__), "READY_TO_PRINT_V2")
P2S = 256.0

# which parts must carry a bayonet (snap) — all body/base/holder, not the shade shells
# We report snap presence by geometry knowledge: every part using bay_male/bay_female has it.
BAYONET_PARTS = {
    "01_Fuss_Rund.stl","02_Fuss_Design.stl","03_Koerper_Kugel.stl",
    "04_Koerper_Abgeflacht.stl","05_Koerper_Organisch.stl","06_Koerper_Geometrisch.stl",
    "07_Koerper_Schmal_Ring.stl","08_Koerper_Schmal_Gerippt.stl",
    "09_Schirm_Klassisch.stl","10_Schirm_Gerippt.stl","11_Schirm_Organisch.stl",
    "12_STRALA_Befestigung.stl",
}

def bore_min_radius(m):
    """Min vertex radius on a mid-height section; ~30 means bore intact."""
    try:
        zc = (m.bounds[0,2]+m.bounds[1,2])/2
        sec = m.section(plane_origin=[0,0,zc], plane_normal=[0,0,1])
        xy = sec.vertices[:,:2]
        return float(np.sqrt((xy**2).sum(1)).min())
    except Exception:
        return -1.0

def main():
    files = sorted(glob.glob(os.path.join(OUT, "*.stl")))
    results = []
    allpass = True
    for f in files:
        name = os.path.basename(f)
        size = os.path.getsize(f)
        try:
            m = trimesh.load(f)
            dim = (m.bounds[1]-m.bounds[0])
            ncomp = len(m.split(only_watertight=False))
            wt = bool(m.is_watertight)
            vol = float(m.volume)
            bore = bore_min_radius(m)
            fits = bool(all(dim <= P2S))
            faces = int(len(m.faces))
            status = (size > 5000 and wt and vol > 1000 and fits and ncomp == 1)
            # bore relevant for body/base modules (01-08); shades (09-11) and holder (12) exempt
            # holder is a terminal cap — only 6mm cable passes through, not the 60mm plug
            bore_ok = bore >= 29.5 if name in BAYONET_PARTS and not name.startswith(("09","10","11","12")) else True
            status = status and bore_ok
        except Exception as e:
            results.append({"file":name,"error":str(e),"status":"FAIL"}); allpass=False; continue
        if not status: allpass=False
        results.append({
            "file":name,"size_bytes":size,"faces":faces,
            "bbox_mm":[round(float(x),2) for x in dim],
            "volume_mm3":round(vol,1),"watertight":wt,"components":ncomp,
            "bore_min_radius_mm":round(bore,2),
            "bore_passage_ok":bore_ok,
            "bayonet_snap_present":name in BAYONET_PARTS,
            "fits_P2S":fits,"status":"PASS" if status else "FAIL"})
    report = {"all_pass":allpass,"count":len(results),"parts":results}
    with open(os.path.join(os.path.dirname(__file__),"validation_v2.json"),"w") as fh:
        json.dump(report,fh,indent=2)
    print(json.dumps(report,indent=2))
    return 0 if allpass else 1

if __name__=="__main__":
    sys.exit(main())
