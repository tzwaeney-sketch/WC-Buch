# Bill of Materials

## Printed parts (per typical lamp)

| Qty | Part | File | Suggested material |
|-----|------|------|--------------------|
| 1 | `lamp_base` | lamp_base.scad | PLA / PETG |
| 1 | `lamp_base_bottom_plate` | lamp_base.scad | PLA / PETG |
| 1 | `lamp_base_weight_insert` (if not using steel) | lamp_base.scad | PLA |
| 1 | `cable_exit_grommet` | lamp_base.scad | PETG / TPU |
| 1–6 | decorative modules (`mod_*`) | round/geometric/organic/utility | PLA / PETG / ASA |
| 1 | `mod_top_cap` | utility_modules.scad | PETG / ASA (near bulb) |
| 2 | `strala_split_clamp_left` + `_right` | strala_holder.scad | PETG |
| 1 | shade (any `shade_*`, ring is integral) | lamp_shades.scad | PETG / ASA |

## Calibration parts (print once, before everything)

| Part | File |
|------|------|
| `passage_test_ring(60)` | calibration_parts.scad |
| `long_tunnel_test` | calibration_parts.scad |
| `bayonet_tolerance_pair(0.20..0.40)` | bayonet_system.scad |
| `bayonet_snap_test` | calibration_parts.scad |
| `strala_fit_test` | strala_holder.scad |
| `cable_exit_test` | calibration_parts.scad |
| `shade_wall_test` | calibration_parts.scad |

## Hardware

| Qty | Item | Notes |
|-----|------|-------|
| 1 | IKEA STRÅLA cord set + LED bulb | original only |
| 1 | Steel ballast ring ~200 g | fits base weight chamber |
| 4 | Rubber feet (~12 mm) | press into base foot pockets |
| 3 | M3 flat-head screws | bottom plate |
| 4 | M3 screws + nuts | STRÅLA split clamp (2 per joint) |
