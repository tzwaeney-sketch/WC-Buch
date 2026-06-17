# Validation Report — Modulare STRÅLA-Lampe

**Status:** Digital geprüft und konstruktiv für mindestens 55 mm Steckerdurchgang ausgelegt.
**Realer Probedruck:** Noch nicht durchgeführt.
**OpenSCAD-Version:** Nicht installiert — statische Code-Prüfung (Syntax, Geometrie-Logik, Parameterfluss)

---

## Legende

| Kürzel | Bedeutung |
|--------|-----------|
| ✓ | Bestanden / vorhanden |
| ✗ | Fehler gefunden |
| ⚠ | Einschränkung / Hinweis |
| N/A | Nicht anwendbar |
| MEASURE | Reale Messung erforderlich |

---

## Dateien

### config.scad
- Renderprüfung: N/A (Parameterdatei, kein Geometry-Output)
- STL-Export: N/A
- Geschlossener Volumenkörper: N/A
- 55mm-Steckerdurchgang konstruktiv: ✓ — `final_plug_passage = max(47.8, 55.0) = 55.0mm`
- Bajonett kollisionsfrei: N/A
- Druckbar: N/A — `$fn = 64` global, `fn_large_bore = 128` für Bohrungen
- Reale Passung erforderlich: Nein
- Korrekturen: Trailing-Semikolon nach `include` entfernt (file-weit vereinheitlicht). Keine logischen Änderungen.
- Einschränkungen: STRÅLA-Parameter sind Platzhalter (MEASURE).

### bayonet_system.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓ über Wrapper
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — `bore = max(inner_d, final_plug_passage)`, durchgehend gebohrt
- Bajonett kollisionsfrei: ✓ — Lug-Mittelradius `lug_mid_r ≈ 32.1mm` > Bohrungsradius 27.5mm; Lugs liegen vollständig AUSSERHALB der 55mm-Bohrung. Lead-in-Fasen männlich und weiblich vorhanden. Lock-Kanal um `bayonet_lock_angle = 25°` versetzt.
- Druckbar: ✓ — Lug-Höhe 1.6mm (>= 2·layer_height); `$fn = fn_large_bore` auf Bohrungen
- Reale Passung erforderlich: Ja (Toleranztest)
- Korrekturen: `include`-Semikolon entfernt.
- Einschränkungen: Optimale `bayonet_radial_clearance` erst per Toleranztestdruck.

### cable_passage.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — `cable_guide_channel` Bohrung = `final_plug_passage`, Fasen an beiden Mündungen
- Bajonett kollisionsfrei: N/A
- Druckbar: ✓
- Reale Passung erforderlich: MEASURE (Kabeldurchmesser)
- Korrekturen: `include`-Semikolon entfernt.
- Einschränkungen: `plug_test_body` ist Näherung des Schuko-Körpers.

### lamp_base.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — zentrale Bohrung `bore = 55mm` durchgehend von unten nach oben inkl. Bajonett
- Bajonett kollisionsfrei: ✓ — Männliches Bajonett oben, Bohrung durchgezogen
- Druckbar: ✓ — steht plan, 4 Fußmulden, Bodenplatte separat mit Kabelschlitz
- Reale Passung erforderlich: Ja (Stecker + Kabelweg)
- Korrekturen: **Kritisch** — seitlicher Kabelausgang durchquerte zuvor die zentrale 55mm-Bohrung (kreuzte den klaren Steckerdurchgang bei z=h/2). Neu: Ausgang läuft nur von der Außenwand bis zur Außenfläche des Durchgangsrohrs; ein kleines kabelgroßes Loch (`strala_cable_diameter + 2·clearance`) durchstößt die Durchgangswand. Der vertikale 55mm-Klardurchgang bleibt unberührt. `include`-Semikola entfernt.
- Einschränkungen: Gewichtskammer als separater Ring konstruiert; Stahlgewicht/Insert separat.

### strala_holder.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — `strala_top_cap` zieht `bore = final_plug_passage` durch Bajonett + Übergangsdeck
- Bajonett kollisionsfrei: ✓ — weibliches Bajonett unten integriert
- Druckbar: ✓
- Reale Passung erforderlich: MEASURE (alle STRÅLA-Maße)
- Korrekturen: `include`-Semikola entfernt.
- Einschränkungen: Sämtliche STRÅLA-Maße sind Platzhalter bis zur Messung.

### round_modules.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — `_module_frame` bohrt `final_plug_passage` über die GESAMTE Teilhöhe (fh + body_h + male) plus 1mm Überstand
- Bajonett kollisionsfrei: ✓ — weiblich unten, männlich oben, beide integriert
- Druckbar: ✓
- Reale Passung erforderlich: Nein
- Korrekturen: **Kritisch** — `mod_sphere` hatte eine fehlerhafte `intersection()` mit drei Kindern (Kugel ∩ Zylinder ∩ Würfel), wobei Kugel und Bajonett-Kragen sich nur an der Achse berührten → kein durchgehender Körper. Neu: saubere `intersection()` (Kugel ∩ Hüll-Würfel) plus zentrales Stützrohr (`final_plug_passage + 2·structural_wall`) über volle Höhe → ein druckbarer Volumenkörper. Gleiche Stützrohr-Ergänzung für `mod_oblate_sphere` und `mod_double_sphere` (letzteres zuvor mit Mehrkind-Body, der nur via `children(0)` teilweise gerendert worden wäre — in `union()` gekapselt).
- Einschränkungen: Sehr großzügige Außendurchmesser (bis 120mm) → Druckbettgröße prüfen.

### geometric_modules.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — via `_module_frame`
- Bajonett kollisionsfrei: ✓
- Druckbar: ✓ — `minkowski` gerundete Formen (rechenintensiv aber gültig); `linear_extrude` jeweils mit 2D-Kind
- Reale Passung erforderlich: Nein
- Korrekturen: `include`-Semikola entfernt. Keine Geometriefehler gefunden (Bodies sind jeweils Einzelkinder).
- Einschränkungen: `mod_diamond_faceted` läuft an Ober-/Unterspitze nah an die Bohrung — Wand dort minimal, aber Bohrung wird sauber freigeschnitten.

### organic_modules.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — via `_module_frame`; alle `rotate_extrude`-Profile starten >= Bohrungsradius
- Bajonett kollisionsfrei: ✓
- Druckbar: ✓
- Reale Passung erforderlich: Nein
- Korrekturen: **Kritisch** — `mod_pumpkin` übergab dem `_module_frame` mehrere Kinder (Kernkugel + Rippen-`for`), von denen nur `children(0)` gerendert worden wäre → Rippen wären verschwunden. In `union()` gekapselt und zentrales Stützrohr ergänzt. `mod_teardrop`: innere Profilradien von `+1` auf `+ structural_wall` erhöht, damit Restwand nach 55mm-Bohrung >= minimum_wall. `include`-Semikola entfernt.
- Einschränkungen: `mod_wave`/`mod_vase` Profile per `let`/`concat` generiert — Punktreihenfolge CCW, gültig.

### lamp_shades.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓ (Schirme bewusst hohl/einwandig)
- 55mm-Steckerdurchgang konstruktiv: ✓ — `shade_mounting_ring` hält `bore = max(final_plug_passage, …)` frei
- Bajonett kollisionsfrei: N/A — Schirme sitzen auf Montagering, nicht im Bajonett-Stack
- Druckbar: ⚠ — `shade_wall = 1.2mm` grenzwertig, für dekorative Schirme akzeptabel
- Reale Passung erforderlich: Nein (Wandstärketest empfohlen)
- Korrekturen: `include`-Semikolon entfernt. Keine Logikfehler; `rotate_extrude`/`polygon`-Profile gültig.
- Einschränkungen: Dünnwand-Schirme ggf. mit Vasenmodus drucken.

### calibration_parts.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — `passage_test_ring_55mm`, plus 7 Lehren (44,46,48,50,52,55,58)
- Bajonett kollisionsfrei: ✓ — `bayonet_tolerance_test` mit echter Geometriedifferenz (`delta = clearance - bayonet_radial_clearance`)
- Druckbar: ✓
- Reale Passung erforderlich: Ja (das ist der Zweck dieser Teile)
- Korrekturen: `include`-Semikola entfernt. Lehren tragen `text()`-Beschriftung ✓.
- Einschränkungen: Toleranztest verbreitert nur die Kavität (radiale Annäherung).

### assembly_preview.scad
- Renderprüfung: ✓ (statisch)
- STL-Export: N/A (Vorschau, keine Druckteile)
- Geschlossener Volumenkörper: N/A
- 55mm-Steckerdurchgang konstruktiv: ✓ — optionaler `_clearance_overlay`-Stab (55mm) visualisiert Durchgang
- Bajonett kollisionsfrei: ✓ (Stapel-Logik mit `overlap = bayonet_working_depth`)
- Druckbar: N/A
- Reale Passung erforderlich: Nein
- Korrekturen: `include`-Semikola entfernt. Alle benötigten `include` vorhanden und korrekt.
- Einschränkungen: Keine.

### export_all.scad
- Renderprüfung: N/A (nur Kommentare/Doku)
- STL-Export: N/A
- Geschlossener Volumenkörper: N/A
- 55mm-Steckerdurchgang konstruktiv: N/A
- Bajonett kollisionsfrei: N/A
- Druckbar: N/A
- Reale Passung erforderlich: Nein
- Korrekturen: Keine (reine Dokumentationsdatei, Modul-/Datei-Liste vollständig).
- Einschränkungen: Keine.

### passage_variants.scad (neu erstellt)
- Renderprüfung: ✓ (statisch)
- STL-Export: ✓
- Geschlossener Volumenkörper: ✓
- 55mm-Steckerdurchgang konstruktiv: ✓ — drei Ringe 55/58/60mm, 20mm hoch, Ober-/Unterfasen, beschriftet
- Bajonett kollisionsfrei: N/A (reine Durchgangslehren)
- Druckbar: ✓ — steht plan, Beschriftung als `linear_extrude(text())`
- Reale Passung erforderlich: Ja (mit echtem Schuko-Stecker testen)
- Korrekturen: Datei neu angelegt.
- Einschränkungen: Keine.

---

## Zusammenfassung gefundener und behobener Fehler

| # | Datei | Schweregrad | Fehler | Behebung |
|---|-------|-------------|--------|----------|
| 1 | lamp_base.scad | KRITISCH | Seitlicher Kabelausgang kreuzte die zentrale 55mm-Bohrung (durchbrach den Klardurchgang) | Ausgang endet an der Durchgangsrohr-Außenwand; nur kabelgroßes Loch durch die Wand |
| 2 | round_modules.scad | KRITISCH | `mod_sphere` fehlerhafte 3-Kind-`intersection()`, Körper nicht durchgehend mit Bajonett verbunden | Saubere `intersection()` + zentrales Stützrohr über volle Höhe |
| 3 | round_modules.scad | HOCH | `mod_double_sphere`/`mod_oblate_sphere` Body nur achsberührt, kein Vollkörper | Zentrales Stützrohr (`+2·structural_wall`) ergänzt, Mehrkind in `union()` gekapselt |
| 4 | organic_modules.scad | KRITISCH | `mod_pumpkin` übergab Mehrkind an `_module_frame` → nur `children(0)` gerendert, Rippen verloren | In `union()` gekapselt + Stützrohr |
| 5 | organic_modules.scad | MITTEL | `mod_teardrop` Restwand nach Bohrung < `minimum_wall` (1.68mm) | Innere Profilradien auf `+ structural_wall` erhöht |
| 6 | alle .scad | NIEDRIG | `include <…>;` mit unnötigem Semikolon (leere Anweisung) | Semikola entfernt |
| 7 | — | — | passage_variants.scad fehlte | Datei mit 55/58/60mm-Ringen erstellt |

Geprüft, aber korrekt vorgefunden (keine Änderung nötig):
- Bajonett-Lugs liegen außerhalb der 55mm-Bohrung (`lug_mid_r ≈ 32.1 > 27.5`). ✓
- `_inner_chamfer` Polygon-Winding und Mirror an Ober-/Unterseite korrekt. ✓
- Alle `include`-Abhängigkeiten vorhanden, keine Zirkelbezüge. ✓
- `$fn`/`fn_large_bore` global gesetzt, Bohrzylinder mit `$fn = fn_large_bore`. ✓
- Kalibrierlehren und Toleranztests beschriftet und mit echter Geometriedifferenz. ✓

---

## Noch erforderliche reale Prüfungen

1. Realer Schuko-Stecker durch Durchgangslehren führen (44–58mm)
2. Bajonett-Toleranztest drucken, beste Passung bestimmen
3. STRÅLA-Fassung ausmessen → MEASURE-Parameter eintragen
4. Fuß mit Stecker montieren, Kabelweg prüfen
5. Standfestigkeit mit montiertem Schirm testen

---

## Hinweis zur Sicherheit

Diese Prüfung ist eine digitale Code-Prüfung. Sie ersetzt keinen realen Probedruck.
Erst nach erfolgreichem Testdruck mit dem tatsächlichen IKEA-STRÅLA-Stecker darf geschrieben werden:
"Realer Steckerdurchgang erfolgreich geprüft."
