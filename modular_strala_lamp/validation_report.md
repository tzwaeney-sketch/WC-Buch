# Validation Report — Modulare STRÅLA-Lampe

**Geprüft:** 2026-06-17 13:40
**OpenSCAD:** 2021.01 (echte Render-Prüfung)
**Mesh-Prüfung:** trimesh (Python)
**Ergebnis:** 54/54 bestanden

> **Digital geprüft und konstruktiv für mindestens 60 mm Steckerdurchgang ausgelegt.**
> Realer Steckerdurchgang-Test noch erforderlich.

## Ergebnistabelle

| Teil | Exit | Manifold | Dateigröße | Status |
|------|------|----------|------------|--------|
| passage_ring_60mm | 0 | True | 330,242 B | PASS |
| passage_ring_55mm | 0 | True | 324,427 B | PASS |
| passage_ring_58mm | 0 | True | 315,006 B | PASS |
| passage_ring_62mm | 0 | True | 316,035 B | PASS |
| long_tunnel_test | 0 | True | 318,815 B | PASS |
| bayonet_snap_test | 0 | True | 474,505 B | PASS |
| shade_wall_test | 0 | True | 314,873 B | PASS |
| cable_exit_test | 0 | True | 45,553 B | PASS |
| bayonet_tolerance_020 | 0 | True | 739,698 B | PASS |
| bayonet_tolerance_025 | 0 | True | 825,533 B | PASS |
| bayonet_tolerance_030 | 0 | True | 764,420 B | PASS |
| bayonet_tolerance_035 | 0 | True | 850,368 B | PASS |
| bayonet_tolerance_040 | 0 | True | 646,323 B | PASS |
| lamp_base | 0 | True | 545,327 B | PASS |
| lamp_base_bottom_plate | 0 | True | 381,676 B | PASS |
| lamp_base_weight_insert | 0 | True | 82,183 B | PASS |
| cable_exit_grommet | 0 | True | 64,369 B | PASS |
| mod_sphere | 0 | True | 1,167,840 B | PASS |
| mod_oblate_sphere | 0 | True | 1,315,827 B | PASS |
| mod_double_sphere | 0 | True | 1,281,532 B | PASS |
| mod_soft_cylinder | 0 | True | 379,225 B | PASS |
| mod_disc | 0 | True | 343,401 B | PASS |
| mod_ring_module | 0 | True | 252,930 B | PASS |
| mod_teardrop | 0 | True | 495,394 B | PASS |
| mod_vase | 0 | True | 921,958 B | PASS |
| mod_pumpkin | 0 | True | 862,895 B | PASS |
| mod_wave | 0 | True | 252,930 B | PASS |
| mod_organic_diamond | 0 | True | 252,930 B | PASS |
| mod_asymmetric_soft | 0 | True | 624,899 B | PASS |
| mod_narrow_shadow_ring | 0 | True | 273,695 B | PASS |
| mod_narrow_ribbed_ring | 0 | True | 325,543 B | PASS |
| mod_cube_rounded | 0 | True | 516,281 B | PASS |
| mod_hexagon | 0 | True | 314,141 B | PASS |
| mod_diamond_faceted | 0 | True | 442,201 B | PASS |
| mod_frustum | 0 | True | 348,986 B | PASS |
| mod_triangle_rounded | 0 | True | 276,838 B | PASS |
| mod_stepped_geometric | 0 | True | 317,791 B | PASS |
| mod_neutral_extension | 0 | True | 273,695 B | PASS |
| mod_short_spacer | 0 | True | 273,695 B | PASS |
| mod_top_cap | 0 | True | 226,237 B | PASS |
| mod_transition | 0 | True | 275,145 B | PASS |
| strala_fit_test | 0 | True | 721,532 B | PASS |
| strala_split_clamp_left | 0 | True | 39,491 B | PASS |
| strala_split_clamp_right | 0 | True | 37,035 B | PASS |
| shade_frustum | 0 | True | 436,803 B | PASS |
| shade_cylinder | 0 | True | 280,526 B | PASS |
| shade_bell | 0 | True | 302,818 B | PASS |
| shade_mushroom | 0 | True | 1,609,181 B | PASS |
| shade_globe | 0 | True | 3,342,694 B | PASS |
| shade_vertical_ribs | 0 | True | 1,001,733 B | PASS |
| shade_horizontal_ribs | 0 | True | 9,274,956 B | PASS |
| shade_faceted | 0 | True | 186,195 B | PASS |
| shade_organic_curve | 0 | True | 110,690 B | PASS |
| shade_perforated | 0 | True | 2,703,768 B | PASS |

## Zusammenfassung

- **Gesamt:** 54 Teile
- **Bestanden:** 54
- **Fehlgeschlagen:** 0

## Hinweis

Diese Prüfung ist eine digitale Render- und Mesh-Prüfung.
Sie ersetzt **keinen** realen Probedruck.
Erst nach erfolgreichem Testdruck mit dem tatsächlichen IKEA-STRÅLA-Stecker
darf geschrieben werden: "Realer Steckerdurchgang erfolgreich geprüft."

## Noch erforderliche reale Prüfungen

1. STRÅLA-Fassung ausmessen -> MEASURE-Parameter in config.scad eintragen
2. 60mm-Durchgangsring drucken und mit realem Stecker prüfen
3. Bajonett-Toleranzset drucken -> bestes Spiel bestimmen
4. Fußkabelweg real montieren und prüfen
5. Standfestigkeit mit montiertem Schirm testen
