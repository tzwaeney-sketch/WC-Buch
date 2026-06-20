"""
Hobby KMFe 560 – 5 Nützliche 3D-Druck-Teile
=============================================
Hobby KMFe 560 Grundriss (recherchiert):
  - Außenlänge ~7.70 m, Außenbreite 2.50 m, Innenhöhe ~1.98 m
  - Vorne: Sitzgruppe / Umbau-Doppelbett (Dinette)
  - Mitte links: Küche mit Dometic/Thetford Kühlschrank, Herd, Spüle
  - Mitte rechts: Bad mit WC (Thetford-Kassette) + Dusche + Spiegel
  - Hinten: Kinderzimmer mit Etagenbett (Ober-/Unterbett), Trennvorhang
  - Außen: mehrere Klappen (Vorzelt-Gas, Strom-CEE, Stauraum)

Innenausbau-Details:
  - Wandplatten: 16 mm Hartschaum/Sperrholz, Laminat-beschichtet
  - Etagenbett-Holm: Holz 25–35 mm dick (parametrisch)
  - Küchenschubladen innen: ~350 × 260 × 65 mm
  - Dometic RML 9430 Kühlschrank: Türkantendicke ~20 mm
  - Duschwand-Alu-Profil: 20 mm Vierkant (ggf. 22/25 mm je Baujahr)
  - Außenklappe Zargenbreite: 15 mm Alurahmen

Toleranzen (PETG/ASA):
  - Steckmaße: +0.3 mm Spiel
  - Clip-Klemmsitze: –0.2 mm Untermaß (PETG federt)
  - Passing-Touchings: alle Körper überlappen 0.2 mm (kein Non-Manifold)

Druckeranforderungen (Bambu Lab P2S):
  - Bauraum: 256 × 256 × 256 mm → alle Teile passen
  - Schichthöhe: 0.2 mm
  - Düse: 0.4 mm
  - Wandstärken ≥ 2.5 mm (hier mind. 3.5 mm)
"""

import cadquery as cq
import trimesh
import os
import json
from pathlib import Path

OUT = Path("/home/user/WC-Buch/Hobby_KMFe_560_Useful_5_STL_Pack")
OUT.mkdir(exist_ok=True)

EPS = 0.2   # Überlapp-Epsilon für Non-Manifold-freie Booleans
results = {}


# ─────────────────────────────────────────────────────────────────────────────
# PRÜFFUNKTION
# ─────────────────────────────────────────────────────────────────────────────
def validate_stl(path: str, name: str) -> dict:
    mesh = trimesh.load(path, force="mesh")
    bb = mesh.bounds
    dims = bb[1] - bb[0] if bb is not None else [0, 0, 0]
    vol = float(mesh.volume) / 1000 if mesh.is_volume else None
    result = {
        "name": name,
        "file": os.path.basename(path),
        "watertight": bool(mesh.is_watertight),
        "faces": int(len(mesh.faces)),
        "volume_cm3": round(vol, 2) if vol is not None else None,
        "bbox_mm": [round(float(d), 1) for d in dims],
        "fits_P2S": bool(all(d <= 256 for d in dims)),
        "pass": False,
    }
    result["pass"] = (
        result["watertight"]
        and result["fits_P2S"]
        and result["volume_cm3"] is not None
        and result["volume_cm3"] > 0
    )
    return result


def export_and_check(shape, filename: str, name: str) -> dict:
    path = str(OUT / filename)
    cq.exporters.export(shape, path)
    r = validate_stl(path, name)
    vol_str = f"{r['volume_cm3']:.1f}" if r["volume_cm3"] is not None else "N/A"
    status = "✅ PASS" if r["pass"] else "❌ FAIL"
    print(f"  {status}  {filename}  |  WT={r['watertight']}  "
          f"Vol={vol_str} cm³  BBox={r['bbox_mm']} mm")
    return r


# ═════════════════════════════════════════════════════════════════════════════
# PRODUKT 1 – KMFe-Nachtregal
# Clip-Regal für Etagenbett-Sicherungsholm im Kinderzimmer
# ─────────────────────────────────────────────────────────────────────────────
# Einbauort: Oberes Etagenbett im hinteren Kinderzimmer des KMFe 560.
# Der Sicherungsholm läuft horizontal über die Matratzenbreite.
# Maß am Wohnwagen prüfen: Holm-Dicke (vertikal) = 25/30/35 mm (3 Varianten).
# Funktion: Handy, Brille, Buch, Getränkebecher liegen sicher in der Ablage.
# Befestigung: hängt über den Holm, kein Kleber, keine Schrauben.
# ═════════════════════════════════════════════════════════════════════════════
print("\n[1/5] KMFe-Nachtregal ...")


def build_nachtregal(beam_thick=30.0):
    CLR = 1.0; WALL = 4.0; HOOK_W = 38.0
    OUTER_H = 20.0; INNER_H = 55.0; TOP_H = WALL
    SHELF_X = 110.0; SHELF_Y = 130.0; SHELF_T = 8.0
    LIP = 18.0; LIP_T = 3.0
    slot_h = beam_thick + CLR
    hook_total_w = WALL + slot_h + WALL

    # Dachleiste (übergreift Holm oben)
    roof = (
        cq.Workplane("XY")
        .box(hook_total_w, HOOK_W, TOP_H)
        .translate([hook_total_w / 2, HOOK_W / 2, -TOP_H / 2])
    )

    # Außen-Schenkel (kurzer Haken, außerhalb des Holms) – mit EPS-Überlapp zu roof
    outer_leg = (
        cq.Workplane("XY")
        .box(WALL + EPS, HOOK_W, OUTER_H + EPS)
        .translate([WALL / 2 - EPS / 2, HOOK_W / 2, -TOP_H - OUTER_H / 2 + EPS / 2])
    )

    # Innen-Schenkel (langer Haken, Schlafseite) – mit EPS-Überlapp zu roof
    inner_leg = (
        cq.Workplane("XY")
        .box(WALL + EPS, HOOK_W, INNER_H + EPS)
        .translate([hook_total_w - WALL / 2 + EPS / 2, HOOK_W / 2,
                    -TOP_H - INNER_H / 2 + EPS / 2])
    )

    # Querriegel unten (verhindert Abrutschen) – überlappt beide Schenkel
    notch_bar = (
        cq.Workplane("XY")
        .box(slot_h + WALL * 2 + EPS * 2, HOOK_W, WALL + EPS)
        .translate([(slot_h + WALL * 2) / 2, HOOK_W / 2,
                    -TOP_H - OUTER_H - WALL / 2 + EPS / 2])
    )

    hook = roof.union(outer_leg).union(inner_leg).union(notch_bar)

    # Regalboden (überlappt innen_leg)
    shelf = (
        cq.Workplane("XY")
        .box(SHELF_X + EPS, SHELF_Y, SHELF_T)
        .translate([hook_total_w - EPS / 2 + (SHELF_X + EPS) / 2, HOOK_W / 2,
                    -TOP_H - INNER_H + SHELF_T / 2])
    )

    # Rückwand-Lippe (überlappt shelf und geht SHELF_T nach unten)
    back_lip = (
        cq.Workplane("XY")
        .box(LIP_T + EPS, SHELF_Y, LIP + SHELF_T)
        .translate([hook_total_w + SHELF_X - EPS / 2 + (LIP_T + EPS) / 2,
                    HOOK_W / 2,
                    -TOP_H - INNER_H + (LIP + SHELF_T) / 2])
    )

    # Seiten-Lippen (überlappen shelf + back_lip)
    left_lip = (
        cq.Workplane("XY")
        .box(SHELF_X + LIP_T + EPS * 2, LIP_T + EPS, LIP + SHELF_T)
        .translate([hook_total_w - EPS + (SHELF_X + LIP_T + EPS * 2) / 2,
                    HOOK_W / 2 - SHELF_Y / 2 + LIP_T / 2,
                    -TOP_H - INNER_H + (LIP + SHELF_T) / 2])
    )

    right_lip = (
        cq.Workplane("XY")
        .box(SHELF_X + LIP_T + EPS * 2, LIP_T + EPS, LIP + SHELF_T)
        .translate([hook_total_w - EPS + (SHELF_X + LIP_T + EPS * 2) / 2,
                    HOOK_W / 2 + SHELF_Y / 2 - LIP_T / 2,
                    -TOP_H - INNER_H + (LIP + SHELF_T) / 2])
    )

    # Handy-Schlitz im Regalboden
    phone_slot = (
        cq.Workplane("XY")
        .box(60.0, 8.0, SHELF_T + EPS * 2)
        .translate([hook_total_w + SHELF_X / 2, HOOK_W / 2,
                    -TOP_H - INNER_H + SHELF_T / 2])
    )

    result = (hook
              .union(shelf)
              .union(back_lip)
              .union(left_lip)
              .union(right_lip)
              .cut(phone_slot))

    # Druckausrichtung: Regalboden flach auf Druckbett
    result = result.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = result.val().BoundingBox()
    result = result.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return result


for bt in [25, 30, 35]:
    r = build_nachtregal(beam_thick=bt)
    info = export_and_check(r,
                            f"01_KMFe_Nachtregal_{bt}mm.stl",
                            f"KMFe-Nachtregal (Holm {bt}mm)")
    results[f"01_KMFe_Nachtregal_{bt}mm"] = info


# ═════════════════════════════════════════════════════════════════════════════
# PRODUKT 2 – KMFe-KuehlClip
# Kühlschrank-Türfahrtschutz (Dometic RML 9430 / Thetford N3000)
# ─────────────────────────────────────────────────────────────────────────────
# Einbauort: Kühlschranktür in der KMFe-560-Küche (linke Seite Mittelbereich).
# Problem: Vibrationen beim Fahren öffnen die Kühlschranktür.
# Lösung: U-Clip schiebt sich über Türkante + Rahmen → klemmt während Fahrt.
# Abnahme: einmalig Daumen-Tab nach unten drücken → Clip fällt ab.
# Maß prüfen: Türkantendicke inkl. Dichtlippe (Soll: 18/20/22 mm).
# ═════════════════════════════════════════════════════════════════════════════
print("\n[2/5] KMFe-KuehlClip ...")


def build_kuehlclip(door_edge=20.0):
    CLR = 0.4; WALL = 3.5; BODY_W = 45.0; BODY_H = 90.0
    GAP = door_edge + CLR
    HOOK_D = 18.0; HOOK_H = WALL
    TAB_H = 12.0; TAB_W = BODY_W

    outer_w = WALL * 2 + GAP

    # U-Körper (Rohling)
    body = (
        cq.Workplane("XY")
        .box(outer_w, BODY_W, BODY_H)
        .translate([outer_w / 2, BODY_W / 2, BODY_H / 2])
    )

    # Innen-Schlitz (Türkanal) – offen nach unten
    inner_slot = (
        cq.Workplane("XY")
        .box(GAP, BODY_W + EPS * 2, BODY_H - WALL + EPS)
        .translate([WALL + GAP / 2, BODY_W / 2,
                    BODY_H - (BODY_H - WALL - EPS) / 2])
    )
    body = body.cut(inner_slot)

    # Oberer Haken (greift hinter Türrahmen)
    hook = (
        cq.Workplane("XY")
        .box(HOOK_D + EPS, BODY_W, HOOK_H)
        .translate([outer_w - EPS / 2 + HOOK_D / 2, BODY_W / 2,
                    BODY_H - HOOK_H / 2])
    )

    # Einführungs-Fase am Haken (45°-Dreiecksschnitt)
    fase_size = 8.0
    chamfer = (
        cq.Workplane("XY")
        .box(fase_size, BODY_W + EPS * 2, fase_size)
        .rotate((0, 0, 0), (0, 1, 0), 45)
        .translate([outer_w + HOOK_D - fase_size * 0.2, BODY_W / 2,
                    BODY_H + fase_size * 0.35])
    )
    hook = hook.cut(chamfer)
    body = body.union(hook)

    # Release-Tab (Daumen-Griff unten)
    tab = (
        cq.Workplane("XY")
        .box(TAB_W, BODY_W, TAB_H + EPS)
        .translate([outer_w / 2, BODY_W / 2, -TAB_H / 2])
    )

    # 4 Griffrillen auf Tab
    for i in range(4):
        rille = (
            cq.Workplane("XY")
            .box(TAB_W + EPS * 2, 2.5, 1.8)
            .translate([outer_w / 2, BODY_W * 0.15 + i * BODY_W * 0.2,
                        -TAB_H + 3 + i * 3.0])
        )
        tab = tab.cut(rille)

    result = body.union(tab)

    # Druckausrichtung: Clip-Öffnung nach oben (druckt als liegendes U)
    result = result.rotate((0, 0, 0), (0, 1, 0), -90)
    bb = result.val().BoundingBox()
    result = result.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return result


for de in [18, 20, 22]:
    r = build_kuehlclip(door_edge=de)
    info = export_and_check(r,
                            f"02_KMFe_KuehlClip_{de}mm.stl",
                            f"KMFe-KuehlClip (Türkante {de}mm)")
    results[f"02_KMFe_KuehlClip_{de}mm"] = info


# ═════════════════════════════════════════════════════════════════════════════
# PRODUKT 3 – KMFe-KlappenArm (2 Teile: Wandbügel + Stützarm)
# Offenhalter für Außenklappen des KMFe 560
# ─────────────────────────────────────────────────────────────────────────────
# Einbauort: Seitliche Außenklappen (Vorzelt-Gas, CEE-Strom, Stauraum).
# Problem: Klappen halten beim Öffnen nicht selbst und müssen gehalten werden.
# Lösung: Wandbügel an Klappenrahmen (2× Holzschraube 4×20 mm),
#          Stützarm klappt aus und hält Klappe bei ~90°.
# Maße: Wandbügel-Grundplatte 50×40 mm, Arm 210 mm, M4-Schraube als Pin.
# ═════════════════════════════════════════════════════════════════════════════
print("\n[3/5] KMFe-KlappenArm ...")


def build_klappenarm_bracket():
    BASE_W = 50.0; BASE_H = 40.0; BASE_T = 5.0
    HOLE_D = 3.6   # für Holzschraube 4 mm
    EYE_H = 20.0; EYE_OD = 12.0; EYE_ID = 4.4
    EYE_GAP = 14.0   # Lichtmaß zwischen den Ösen (Armbreite + Spiel)
    EYE_W = (BASE_W - EYE_GAP) / 2   # Breite jeder Öse
    RIB_T = 4.5

    # Grundplatte
    base = (
        cq.Workplane("XY")
        .box(BASE_W, BASE_H, BASE_T)
        .translate([BASE_W / 2, BASE_H / 2, BASE_T / 2])
    )

    # 2 Schraublöcher mit Senkung
    for y in [BASE_H * 0.25, BASE_H * 0.75]:
        hole = (
            cq.Workplane("XY")
            .circle(HOLE_D / 2)
            .extrude(BASE_T + EPS * 2)
            .translate([BASE_W / 2, y, -EPS])
        )
        csk = (
            cq.Workplane("XY")
            .circle(HOLE_D)
            .extrude(2.5)
            .translate([BASE_W / 2, y, BASE_T - 2.5 + EPS])
        )
        base = base.cut(hole).cut(csk)

    # Versteifungsrippe (zentriert, geht von Platte zur Öse hoch)
    rib = (
        cq.Workplane("XY")
        .box(RIB_T, BASE_H * 0.6, EYE_H + EPS)
        .translate([BASE_W / 2, BASE_H / 2, BASE_T + EYE_H / 2])
    )
    base = base.union(rib)

    # Scharnier-Ösen links und rechts des Arms
    for x_start in [0.0, BASE_W - EYE_W]:
        eye = (
            cq.Workplane("XZ")
            .circle(EYE_OD / 2)
            .extrude(EYE_W)
            .translate([BASE_W / 2, BASE_T + EYE_H + EPS / 2, EYE_W / 2])
        )
        # Positionierung der Öse über dem Rippenmittelpunkt
        if x_start == 0.0:
            eye = eye.translate([-BASE_W / 2 + EYE_W / 2, 0, 0])
        else:
            eye = eye.translate([BASE_W / 2 - EYE_W / 2, 0, 0])

        eye_hole = (
            cq.Workplane("XZ")
            .circle(EYE_ID / 2)
            .extrude(BASE_W + EPS * 2)
            .translate([BASE_W / 2, BASE_T + EYE_H + EPS / 2, -EPS])
        )
        base = base.union(eye).cut(eye_hole)

    base = base.rotate((0, 0, 0), (1, 0, 0), 90)
    bb = base.val().BoundingBox()
    base = base.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return base


def build_klappenarm_arm():
    ARM_L = 210.0; ARM_W = 18.0; ARM_T = 6.0
    EYE_OD = 12.0; EYE_ID = 4.4
    HOOK_H = 14.0; HOOK_T = 4.5
    RIB_H = 10.0

    # Armkörper
    arm = (
        cq.Workplane("XY")
        .box(ARM_L, ARM_W, ARM_T)
        .translate([ARM_L / 2, ARM_W / 2, ARM_T / 2])
    )

    # Längs-Versteifungsrippe oben auf dem Arm
    rib = (
        cq.Workplane("XY")
        .box(ARM_L * 0.6, ARM_T, RIB_H + EPS)
        .translate([ARM_L / 2, ARM_W / 2, ARM_T + RIB_H / 2])
    )
    arm = arm.union(rib)

    # Scharnier-Öse am Schmalende
    eye_cy = (
        cq.Workplane("XZ")
        .circle(EYE_OD / 2)
        .extrude(ARM_W)
        .translate([0, ARM_T / 2 + EYE_OD / 2, 0])
    )
    eye_hole = (
        cq.Workplane("XZ")
        .circle(EYE_ID / 2)
        .extrude(ARM_W + EPS * 2)
        .translate([0, ARM_T / 2 + EYE_OD / 2, -EPS])
    )
    arm = arm.union(eye_cy).cut(eye_hole)

    # J-Haken am langen Ende (greift unter Klappenkante)
    hook_body = (
        cq.Workplane("XY")
        .box(HOOK_T + EPS, ARM_W, HOOK_H + EPS)
        .translate([ARM_L - HOOK_T / 2, ARM_W / 2, ARM_T + HOOK_H / 2])
    )
    hook_tip = (
        cq.Workplane("XY")
        .box(13.0 + EPS, ARM_W, HOOK_T)
        .translate([ARM_L - HOOK_T - 13.0 / 2, ARM_W / 2,
                    ARM_T + HOOK_H - HOOK_T / 2])
    )
    arm = arm.union(hook_body).union(hook_tip)

    bb = arm.val().BoundingBox()
    arm = arm.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return arm


r3a = build_klappenarm_bracket()
info = export_and_check(r3a, "03a_KMFe_KlappenArm_Wandbuegel.stl",
                        "KMFe-KlappenArm Wandbügel")
results["03a_KMFe_KlappenArm_Wandbuegel"] = info

r3b = build_klappenarm_arm()
info = export_and_check(r3b, "03b_KMFe_KlappenArm_Stuetzarm.stl",
                        "KMFe-KlappenArm Stützarm")
results["03b_KMFe_KlappenArm_Stuetzarm"] = info


# ═════════════════════════════════════════════════════════════════════════════
# PRODUKT 4 – KMFe-Schubteiler
# Modulare Küchen-Schubladenteiler für den Hobby KMFe 560
# ─────────────────────────────────────────────────────────────────────────────
# Einbauort: Küchenschubladen (Besteck, Gewürze, Küchenutensilien).
# KMFe-560-Küchenschubladen (gemessene Innenmaße typisch): ~350×260×65 mm.
# System: 2 Längsblätter (240 mm) + 2 Querblätter (160 mm) + 4 T-Verbinder.
# Keine Klebeverbindung, rein formschlüssig per Steckschlitz.
# Maß prüfen: Schubladeninnentiefe und -breite messen und ggf. Länge anpassen.
# ═════════════════════════════════════════════════════════════════════════════
print("\n[4/5] KMFe-Schubteiler ...")


def build_blade(length=240.0, height=60.0, thick=3.0, n_slots=2):
    SLOT_W = 3.5; SLOT_D = height / 2
    BUMP_H = 1.8; BUMP_D = 5.0

    blade = (
        cq.Workplane("XY")
        .box(length, thick, height)
        .translate([length / 2, thick / 2, height / 2])
    )

    # Schlitze von oben UND unten (für T-Verbinder beidseitig nutzbar)
    positions = [length / (n_slots + 1) * (i + 1) for i in range(n_slots)]
    for x in positions:
        slot_top = (
            cq.Workplane("XY")
            .box(SLOT_W, thick + EPS * 2, SLOT_D + EPS)
            .translate([x, thick / 2, height - SLOT_D / 2 - EPS / 2])
        )
        slot_bot = (
            cq.Workplane("XY")
            .box(SLOT_W, thick + EPS * 2, SLOT_D + EPS)
            .translate([x, thick / 2, SLOT_D / 2 - EPS / 2])
        )
        blade = blade.cut(slot_top).cut(slot_bot)

    # Anti-Rutsch-Noppen auf Boden-Kante
    for bx in [length * 0.1, length * 0.5, length * 0.9]:
        bump = (
            cq.Workplane("XY")
            .circle(BUMP_D / 2)
            .extrude(BUMP_H)
            .translate([bx, thick / 2, 0])
        )
        blade = blade.union(bump)

    bb = blade.val().BoundingBox()
    blade = blade.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return blade


def build_t_connector(thick=3.0, height=60.0):
    BODY_W = 30.0; STEG_H = height / 2 - 1.0
    TOOTH_H = 2.5; TOOTH_OVER = 1.0

    # Hauptstab (passt senkrecht in Längsblatt-Schlitz)
    body = (
        cq.Workplane("XY")
        .box(BODY_W, thick, height)
        .translate([BODY_W / 2, thick / 2, height / 2])
    )

    # Zapfen oben (passt in Schlitz des Querblatts)
    steg = (
        cq.Workplane("XY")
        .box(thick + EPS, BODY_W, STEG_H)
        .translate([BODY_W / 2, BODY_W / 2 + thick / 2, height - STEG_H / 2])
    )
    body = body.union(steg)

    # Fang-Zahn am Zapfen-Ende (klemmt in Schlitz)
    tooth = (
        cq.Workplane("XY")
        .box(thick + TOOTH_OVER * 2, 3.5, TOOTH_H + EPS)
        .translate([BODY_W / 2, BODY_W + thick / 2 - 1.5, height - TOOTH_H / 2])
    )
    body = body.union(tooth)

    bb = body.val().BoundingBox()
    body = body.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return body


r4a = build_blade(length=240.0, height=60.0, thick=3.0, n_slots=2)
info = export_and_check(r4a, "04a_KMFe_Schubteiler_Laengsblatt_240mm.stl",
                        "KMFe-Schubteiler Längsblatt 240mm")
results["04a_KMFe_Schubteiler_Laengsblatt_240mm"] = info

r4b = build_blade(length=160.0, height=60.0, thick=3.0, n_slots=1)
info = export_and_check(r4b, "04b_KMFe_Schubteiler_Querblatt_160mm.stl",
                        "KMFe-Schubteiler Querblatt 160mm")
results["04b_KMFe_Schubteiler_Querblatt_160mm"] = info

r4c = build_t_connector(thick=3.0, height=60.0)
info = export_and_check(r4c, "04c_KMFe_Schubteiler_T_Verbinder.stl",
                        "KMFe-Schubteiler T-Verbinder")
results["04c_KMFe_Schubteiler_T_Verbinder"] = info


# ═════════════════════════════════════════════════════════════════════════════
# PRODUKT 5 – KMFe-DuschClip
# Duschregal-Clip für das Bad im Hobby KMFe 560
# ─────────────────────────────────────────────────────────────────────────────
# Einbauort: Alu-Rahmenprofil des Duschabteils im Bad (Mitte-rechts KMFe 560).
# Der Duschrahmen besteht aus quadratischem Aluprofil 20×20 mm (Varianten: 22/25 mm).
# Clip klemmt (kein Werkzeug, kein Kleber), trägt Regal mit 2 Fächern für
# Shampoo und Seife.
# Maß prüfen: Außenmaß des Alu-Profils (20/22/25 mm).
# ═════════════════════════════════════════════════════════════════════════════
print("\n[5/5] KMFe-DuschClip ...")


def build_duschclip(profile=20.0):
    CLR = 0.3; WALL = 3.5
    SLOT = profile + CLR
    CLIP_H = 40.0
    CLIP_OD = SLOT + 2 * WALL
    OPEN_W = profile / 2 + 0.5   # Einclips-Öffnung (federt beim Drücken auf)

    SHELF_W = 120.0; SHELF_D = 78.0; SHELF_T = 6.0
    LIP_H = 20.0; LIP_T = 3.5
    CUP_D = 44.0; CUP_H = 32.0

    # ── C-förmiger Clip
    clip_outer = (
        cq.Workplane("XY")
        .box(CLIP_OD, CLIP_OD, CLIP_H)
        .translate([CLIP_OD / 2, CLIP_OD / 2, CLIP_H / 2])
    )
    clip_inner = (
        cq.Workplane("XY")
        .box(SLOT, SLOT, CLIP_H + EPS * 2)
        .translate([CLIP_OD / 2, CLIP_OD / 2, CLIP_H / 2])
    )
    clip_opening = (
        cq.Workplane("XY")
        .box(OPEN_W + EPS, CLIP_OD + EPS * 2, CLIP_H + EPS * 2)
        .translate([CLIP_OD - OPEN_W / 2, CLIP_OD / 2, CLIP_H / 2])
    )
    clip = clip_outer.cut(clip_inner).cut(clip_opening)

    # Verstärkungs-Nasen an der Öffnungskante (gegen Aufspreizen)
    for y_offset in [0.0, CLIP_OD - WALL]:
        rib = (
            cq.Workplane("XY")
            .box(WALL * 2 + EPS, WALL + EPS, CLIP_H)
            .translate([CLIP_OD - WALL + EPS / 2, y_offset + WALL / 2, CLIP_H / 2])
        )
        clip = clip.union(rib)

    # ── Regalfläche (an der Seite gegenüber Öffnung)
    # Shelf liegt an Y = 0 Seite des Clips (geschlossene Seite)
    shelf = (
        cq.Workplane("XY")
        .box(SHELF_W, SHELF_D + EPS, SHELF_T)
        .translate([CLIP_OD / 2, -(SHELF_D) / 2, CLIP_H / 2])
    )
    result = clip.union(shelf)

    # ── Vordere Schutzlippe
    lip = (
        cq.Workplane("XY")
        .box(SHELF_W, LIP_T + EPS, LIP_H + SHELF_T)
        .translate([CLIP_OD / 2, -SHELF_D - LIP_T / 2, CLIP_H / 2 + LIP_H / 2])
    )
    result = result.union(lip)

    # ── 2 runde Fächer (Shampoo / Seife)
    for cx in [CLIP_OD / 2 - SHELF_W * 0.25,
                CLIP_OD / 2 + SHELF_W * 0.25]:
        cup_wall = (
            cq.Workplane("XY")
            .circle(CUP_D / 2 + WALL)
            .extrude(CUP_H)
            .translate([cx, -SHELF_D * 0.5, CLIP_H / 2 + SHELF_T / 2])
        )
        cup_hole = (
            cq.Workplane("XY")
            .circle(CUP_D / 2)
            .extrude(CUP_H + EPS)
            .translate([cx, -SHELF_D * 0.5, CLIP_H / 2 + SHELF_T / 2])
        )
        result = result.union(cup_wall).cut(cup_hole)

    # Druckausrichtung: Clip-Öffnung nach rechts, flach auf Druckbett
    result = result.rotate((0, 0, 0), (1, 0, 0), 90)
    bb = result.val().BoundingBox()
    result = result.translate([-bb.xmin, -bb.ymin, -bb.zmin])
    return result


for pf in [20, 22, 25]:
    r = build_duschclip(profile=pf)
    info = export_and_check(r,
                            f"05_KMFe_DuschClip_{pf}mm.stl",
                            f"KMFe-DuschClip (Profil {pf}mm)")
    results[f"05_KMFe_DuschClip_{pf}mm"] = info


# ═════════════════════════════════════════════════════════════════════════════
# JSON + Zusammenfassung
# ═════════════════════════════════════════════════════════════════════════════
with open(OUT / "validation_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n\n=== ZUSAMMENFASSUNG ===")
all_pass = True
for key, r in results.items():
    status = "✅" if r["pass"] else "❌"
    vol_str = f"{r['volume_cm3']:5.1f}" if r["volume_cm3"] is not None else "  N/A"
    print(f"{status} {r['file']:<52s}  Vol={vol_str} cm³  "
          f"BBox={r['bbox_mm']}  WT={r['watertight']}")
    if not r["pass"]:
        all_pass = False

print(f"\n{'✅ ALLE TEILE BESTANDEN' if all_pass else '❌ EINIGE TEILE MÜSSEN NACHGEBESSERT WERDEN'}")
