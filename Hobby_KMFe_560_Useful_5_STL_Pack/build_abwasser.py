"""
KMFe-AbwasserKupplung – Bajonett-Schnellkupplung für Folienschlauch
====================================================================
Hobby KMFe 560 Abwasserstutzen:   40 mm Außen-Ø (grauer Kunststoffstutzen)
Folienschlauch:                    50 mm Ø (dünne Folienschlauch-Rolle)

Teil A – Fahrzeugteil (bleibt permanent am Wohnwagen):
  - Hülse über 40mm-Stutzen, Bajonett-Aufnahme unten
  - Befestigung: 2× Holzschraube 4×16mm (optional für extra Sicherheit)

Teil B – Schlauchteil (bleibt permanent am Folienschlauch-Ende):
  - Barb-Zapfen (geht in 50mm-Folienschlauch), Bajonett-Pins oben
  - Folienschlauch einmal auf den Zapfen drücken, sitzt dauerhaft

Kuppeln: Teil B mit Folienschlauch hochdrücken → 45° drehen → eingerastet.
Trennen: 45° zurück → abziehen. 3 Sekunden.

Material: PETG (flexibel genug für Clip-Effekt, feuchtigkeitsbeständig)
Toleranzen: Stutzen-Spiel 0.6mm | Bajonett-Spiel 0.5mm | Schlauch-Barbs +1mm
"""

import cadquery as cq
import trimesh
import math
import os
from pathlib import Path

OUT = Path("/home/user/WC-Buch/Hobby_KMFe_560_Useful_5_STL_Pack")
EPS = 0.3

def validate(path, name):
    m = trimesh.load(path, force="mesh")
    dims = m.bounds[1] - m.bounds[0] if m.bounds is not None else [0,0,0]
    vol = float(m.volume)/1000 if m.is_volume else None
    ok = m.is_watertight and vol and vol > 0 and all(d <= 256 for d in dims)
    vol_s = f"{vol:.1f}" if vol else "N/A"
    print(f"  {'✅ PASS' if ok else '❌ FAIL'}  {os.path.basename(path)}  "
          f"WT={m.is_watertight}  Vol={vol_s}cm³  BBox={[round(float(d),1) for d in dims]}")
    return ok

# ─────────────────────────────────────────────────────────────────────────────
# Parameter
# ─────────────────────────────────────────────────────────────────────────────
STUB_OD      = 40.0    # Stutzen Außen-Ø
STUB_CLR     = 0.6     # Spiel Stutzen→Hülse
SLEEVE_WALL  = 7.0     # Wandstärke obere Hülse
SLEEVE_H     = 55.0    # Länge der oberen Hülse (greift über Stutzen)

SKIRT_ID     = 62.0    # Innendurchmesser der Bajonett-Schürze
SKIRT_WALL   = 6.0     # Wandstärke Schürze
SKIRT_H      = 30.0    # Höhe der Bajonett-Schürze
SKIRT_OD     = SKIRT_ID + 2 * SKIRT_WALL   # = 74 mm

PIN_D        = 6.0     # Bajonett-Zapfen Durchmesser
PIN_CLR      = 0.5     # Spiel Zapfen in Nut
PIN_L        = 5.5     # Zapfen-Länge (radiale Projektion in Schlitz)
ENTRY_H      = 14.0    # Vertikaler Einführ-Hub im Bajonett
LOCK_H       = 5.0     # Höhe der horizontalen Rastnut
LOCK_DEG     = 45.0    # Drehwinkel zum Einrasten

PLUG_OD      = SKIRT_ID - 1.0   # = 61 mm (0.5mm Spiel je Seite in Schürze)
PLUG_H       = SKIRT_H - 4.0    # = 26 mm  (Stecker etwas kürzer als Schürze)
BORE_ID      = 42.0              # Innendurchmesser Wasserkanal

HOSE_OD      = 50.0   # Folienschlauch Außen-Ø
BARB_TIP     = 51.0   # Widerhaken Spitze Ø (1mm über Schlauch → klemmt)
BARB_BASE    = 44.0   # Zapfen-Anfang Ø (einfacher Einsteckstart)
BARB_MID     = 47.0   # Zwischen den Widerhaken Ø
BARB_L       = 60.0   # Länge des Schlauch-Zapfens
N_BARBS      = 3      # Anzahl Widerhaken

SCREW_D      = 3.8    # Loch für Holzschraube 4mm (Ø 3.8mm)

# ─────────────────────────────────────────────────────────────────────────────
# TEIL A  –  Fahrzeugteil (Receiver / Aufnahme)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Teil A] Fahrzeugteil ...")

def build_part_a():
    SLEEVE_ID = STUB_OD + STUB_CLR   # = 40.6 mm

    # ── Obere Hülse (geht über den 40mm Stutzen)
    sleeve_outer = (
        cq.Workplane("XY")
        .circle((SLEEVE_ID + 2 * SLEEVE_WALL) / 2)
        .extrude(SLEEVE_H)
    )
    sleeve_bore = (
        cq.Workplane("XY")
        .circle(SLEEVE_ID / 2)
        .extrude(SLEEVE_H + EPS)
    )
    sleeve = sleeve_outer.cut(sleeve_bore)

    # Innen-Rippen für besseren Grip am Stutzen (3× Rippen, 0.5mm Übermaß)
    for angle in [0, 120, 240]:
        rib = (
            cq.Workplane("XY")
            .box(1.0, 6.0, SLEEVE_H * 0.6)
            .translate([SLEEVE_ID / 2 - 0.3, 0, SLEEVE_H * 0.25])
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        sleeve = sleeve.union(rib)

    # 2 Schraublöcher für optionale Holzschrauben (seitlich, 90° versetzt)
    for angle in [45, 225]:
        screw_hole = (
            cq.Workplane("XZ")
            .circle(SCREW_D / 2)
            .extrude((SLEEVE_ID + 2 * SLEEVE_WALL) / 2 + EPS)
            .translate([0, 0, SLEEVE_H * 0.35])
            .rotate((0, 0, SLEEVE_H * 0.35), (0, 0, 1), angle)
        )
        sleeve = sleeve.cut(screw_hole)

    # ── Übergangskonus (Hülse → Schürze)
    cone_h = 10.0
    # Äußerer Übergang
    outer_a_r = (SLEEVE_ID + 2 * SLEEVE_WALL) / 2
    outer_b_r = SKIRT_OD / 2
    cone_outer = (
        cq.Workplane("XY")
        .workplane(offset=-cone_h)
        .circle(outer_a_r)
        .workplane(offset=cone_h)
        .circle(outer_b_r)
        .loft()
        .translate([0, 0, -cone_h])
    )
    cone_bore = (
        cq.Workplane("XY")
        .workplane(offset=-cone_h - EPS)
        .circle(SLEEVE_ID / 2)
        .workplane(offset=cone_h + EPS)
        .circle(SKIRT_ID / 2)
        .loft()
        .translate([0, 0, -cone_h])
    )
    cone = cone_outer.cut(cone_bore)

    # ── Bajonett-Schürze (unten)
    skirt_outer = (
        cq.Workplane("XY")
        .circle(SKIRT_OD / 2)
        .extrude(SKIRT_H)
        .translate([0, 0, -SKIRT_H - cone_h])
    )
    skirt_bore = (
        cq.Workplane("XY")
        .circle(SKIRT_ID / 2)
        .extrude(SKIRT_H + EPS)
        .translate([0, 0, -SKIRT_H - cone_h])
    )
    skirt = skirt_outer.cut(skirt_bore)

    part_a = sleeve.union(cone).union(skirt)

    # ── Bajonett-Schlitze (3×, 120°-Teilung)
    # Jeder Schlitz: vertikaler Einführspalt (von unten) + horizontale Rastnut (45°)
    slot_depth = SKIRT_WALL + EPS * 2   # schlitzt durch die gesamte Schürzenwand
    slot_r     = SKIRT_ID / 2 + SKIRT_WALL / 2  # Mitte der Schürzenwand im Radius

    # Chord-Länge für 45° am Schürzen-Innenradius
    r_inner = SKIRT_ID / 2
    chord = 2 * r_inner * math.sin(math.radians(LOCK_DEG / 2))
    # Etwas größer damit der Zapfen auch bei Fertigungstoleranz nicht klemmt
    slot_chord_w = chord + PIN_D + PIN_CLR * 2

    for angle in [0, 120, 240]:
        # Vertikaler Einführspalt (von unten bis ENTRY_H)
        z_base = -SKIRT_H - cone_h
        v_slot = (
            cq.Workplane("XY")
            .box(slot_depth, PIN_D + PIN_CLR, ENTRY_H + EPS)
            .translate([slot_r, 0, z_base + (ENTRY_H + EPS) / 2])
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )

        # Horizontale Rastnut (45° bogen, als Chord-Box approximiert)
        h_slot = (
            cq.Workplane("XY")
            .box(slot_depth, slot_chord_w, LOCK_H + EPS)
            .translate([slot_r, slot_chord_w / 2 - (PIN_D + PIN_CLR) / 2,
                        z_base + ENTRY_H - EPS / 2 + (LOCK_H + EPS) / 2])
            .rotate((0, 0, 0), (0, 0, 1), angle + LOCK_DEG / 2)
        )

        part_a = part_a.cut(v_slot).cut(h_slot)

    # Druckausrichtung: Oben (Stutzen-Seite) auf Druckbett
    part_a = part_a.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = part_a.val().BoundingBox()
    part_a = part_a.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return part_a


part_a = build_part_a()
cq.exporters.export(part_a, str(OUT / "06_KMFe_AbwasserKupplung_TeilA_Fahrzeug.stl"))
validate(str(OUT / "06_KMFe_AbwasserKupplung_TeilA_Fahrzeug.stl"), "Teil A Fahrzeugteil")


# ─────────────────────────────────────────────────────────────────────────────
# TEIL B  –  Schlauchteil (Stecker / Plug)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Teil B] Schlauchteil ...")

def build_part_b():
    # ── Oberer Bajonett-Stecker (geht in Teil A Schürze)
    plug_outer = (
        cq.Workplane("XY")
        .circle(PLUG_OD / 2)
        .extrude(PLUG_H)
    )
    plug_bore = (
        cq.Workplane("XY")
        .circle(BORE_ID / 2)
        .extrude(PLUG_H + EPS)
    )
    plug = plug_outer.cut(plug_bore)

    # ── 3 Bajonett-Zapfen (radial nach außen, mit EPS-Überlapp in Plug)
    pin_z = PLUG_H - ENTRY_H / 2
    for angle in [0, 120, 240]:
        pin = (
            cq.Workplane("YZ")
            .circle(PIN_D / 2)
            .extrude(PIN_L + EPS)               # EPS = Überlapp in Plug-Wand
            .translate([PLUG_OD / 2 - EPS, 0, pin_z])
            .rotate((0, 0, pin_z), (0, 0, 1), angle)
        )
        plug = plug.union(pin)

    # Übergangskonus Stecker → Barb-Zapfen (mit Überlapp zu Plug-Boden)
    trans_h = 8.0
    trans = (
        cq.Workplane("XY")
        .workplane(offset=-trans_h)
        .circle(BARB_BASE / 2)
        .workplane(offset=trans_h + EPS)        # EPS = Überlapp in Plug
        .circle(PLUG_OD / 2 + EPS)
        .loft()
        .translate([0, 0, -trans_h])
    )
    trans_bore = (
        cq.Workplane("XY")
        .circle(BORE_ID / 2)
        .extrude(trans_h + EPS * 2)
        .translate([0, 0, -trans_h - EPS])
    )
    trans = trans.cut(trans_bore)
    plug = plug.union(trans)

    # ── Barb-Zapfen (geht in 50mm Folienschlauch)
    # Aufbau (von Kupplung aus nach unten):
    #  0–10 mm: Einführkonus 44→47 mm
    # 10–15 mm: Widerhaken 1  47→51→47 mm
    # 15–32 mm: Hauptteil 47 mm
    # 32–37 mm: Widerhaken 2  47→51→47 mm
    # 37–54 mm: Hauptteil 47 mm
    # 54–59 mm: Widerhaken 3  47→51→47 mm
    # 59–65 mm: Ende 47 mm

    barb_z = -trans_h

    # Basiszylinder mit Überlapp in Übergangskonus
    barb_base_cyl = (
        cq.Workplane("XY")
        .circle(BARB_MID / 2)
        .extrude(BARB_L + EPS)
        .translate([0, 0, barb_z - BARB_L])
    )
    barb_bore = (
        cq.Workplane("XY")
        .circle(BORE_ID / 2)
        .extrude(BARB_L + EPS * 2)
        .translate([0, 0, barb_z - BARB_L])
    )
    barb = barb_base_cyl.cut(barb_bore)

    # Einführkonus (mit Überlapp in Basiszylinder oben und unten)
    intro = (
        cq.Workplane("XY")
        .workplane(offset=-10)
        .circle(BARB_BASE / 2)
        .workplane(offset=10 + EPS)
        .circle(BARB_MID / 2 + EPS)
        .loft()
        .translate([0, 0, barb_z - 10])
    )
    intro_bore = (
        cq.Workplane("XY")
        .circle(BORE_ID / 2)
        .extrude(12 + EPS)
        .translate([0, 0, barb_z - 10 - EPS])
    )
    barb = barb.union(intro).cut(intro_bore)

    # 3 Widerhaken-Ringe (mit Überlapp in Basiszylinder)
    for pos in [15.0, 32.0, 49.0]:
        bh = 5.0
        br = (
            cq.Workplane("XY")
            .workplane(offset=-(bh + EPS))
            .circle(BARB_MID / 2 + EPS)
            .workplane(offset=bh * 0.7)
            .circle(BARB_TIP / 2)
            .workplane(offset=bh * 0.3 + EPS)
            .circle(BARB_MID / 2 + EPS)
            .loft()
            .translate([0, 0, barb_z - pos])
        )
        br_bore = (
            cq.Workplane("XY")
            .circle(BORE_ID / 2)
            .extrude(bh + EPS * 2)
            .translate([0, 0, barb_z - pos - EPS])
        )
        barb = barb.union(br).cut(br_bore)

    part_b = plug.union(barb)

    # Druckausrichtung: Bajonett-Seite auf Druckbett
    part_b = part_b.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = part_b.val().BoundingBox()
    part_b = part_b.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return part_b


part_b = build_part_b()
cq.exporters.export(part_b, str(OUT / "06_KMFe_AbwasserKupplung_TeilB_Schlauch.stl"))
validate(str(OUT / "06_KMFe_AbwasserKupplung_TeilB_Schlauch.stl"), "Teil B Schlauchteil")

print("\n✅ Fertig.")
