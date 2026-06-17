# Bill of Materials

## Printed parts (per typical lamp)

| Qty | Part | File | Suggested material |
|-----|------|------|--------------------|
| 1 | `lamp_base` | lamp_base.scad | PLA / PETG |
| 1 | `lamp_base_bottom_plate` | lamp_base.scad | PLA / PETG |
| 1 | `lamp_base_weight_insert` (if not using steel) | lamp_base.scad | PLA (or replace w/ steel) |
| 1 | `cable_strain_relief_insert` | lamp_base.scad | PETG |
| 1–4 | decorative modules (any of `mod_*`) | round/geometric/organic_modules.scad | PLA / PETG / ASA |
| 1 | `strala_top_cap` | strala_holder.scad | PETG / ASA (near bulb) |
| 0–1 | `strala_clamp_adapter` | strala_holder.scad | PETG |
| 0–1 | `strala_shade_ring_adapter` | strala_holder.scad | PETG |
| 1 | shade (any `shade_*`, ring is integral) | lamp_shades.scad | PETG / ASA |

## Calibration parts (print once, before everything)

| Part | File |
|------|------|
| `plug_gauge_set` | calibration_parts.scad |
| `passage_test_ring_55mm` | calibration_parts.scad |
| `bayonet_tolerance_set` | calibration_parts.scad |
| `strala_fit_test_ring` | calibration_parts.scad |
| `cable_exit_test` | calibration_parts.scad |
| `shade_wall_test` | calibration_parts.scad |

## Hardware

| Qty | Item | Notes |
|-----|------|-------|
| 3 | M3 x 10 mm countersunk/socket screws | bottom plate |
| 0–2 | M3 x 12 mm + nuts | STRALA clamp adapter (optional) |
| 4 | self-adhesive rubber feet, ~12 mm | base recesses |
| 1 | IKEA STRALA cord set (socket + switch + Schuko plug) | the wiring |
| 1 | LED bulb, <= 7 W, E14/E27 to suit socket | see safety.md |
| 1 | steel ballast ring (optional, replaces printed weight insert) | matches `lamp_base_weight_insert` dims |

## Filament estimate (rough, per part)

| Part class | Est. filament |
|------------|---------------|
| Base assembly | 120–180 g |
| One module | 40–90 g |
| One shade (thin wall) | 50–110 g |
| Full calibration set | ~60 g |
