# Modular STRÅLA Lamp System

A fully parametric, 3D-printable modular table lamp built around IKEA STRÅLA
cord/socket hardware. Decorative modules stack via a twist-lock **bayonet**
interface so you can build endless lamp shapes from a shared kit.

## The one rule that drives everything

> **A complete Schuko plug must pass through every single part — without
> disassembling anything.**

The central clear bore is **never smaller than 60 mm** anywhere in the system.
You can thread an already-wired cable (plug attached) up through the base, every
module, the top cap, and out to the STRÅLA socket. No cutting the cable, no
rewiring.

The clearance math lives in `openscad/config.scad`:

```
calculated_plug_passage = max(width, height, diagonal) + 2 * clearance
                        = max(41.8, 41.8, 41.8) + 2 * 3.0 = 47.8 mm
final_plug_passage      = max(47.8, 60.0) = 60.0 mm   <-- governs all bores
```

A render-time `echo`/`assert` in `config.scad` fails the build if this ever
drops below 60 mm.

## Architecture

```
config.scad            central parameters (edit here)
bayonet_system.scad    male/female bayonet + shared _module_shell() helper
lamp_base.scad         weighted base, bottom plate, weight insert, grommet
round_modules.scad     6 rounded decorative modules
geometric_modules.scad 6 geometric decorative modules
organic_modules.scad   6 organic + 2 narrow accent modules
utility_modules.scad   extension, spacer, top cap, transition
strala_holder.scad     split clamp adapter + fit-test set
lamp_shades.scad       10 shades, each with integral mounting ring
calibration_parts.scad print-first test parts
passage_variants.scad  55/58/60 reference rings
assembly_preview.scad  5 stacked configurations
```

## Bayonet interface

- 3 lugs, 120° apart, 25° twist to lock.
- All lug geometry lives **in the wall** between the 60 mm bore and the 78.4 mm
  interface OD — the lugs never intrude into the clear passage.
- Tolerance set (0.20–0.40 mm) lets you dial in the fit for your printer.

## Quick start

1. Print the **calibration parts** first (see `calibration_parts.scad`).
2. Push your real plug through `passage_test_ring(60)` to confirm clearance.
3. Print the bayonet tolerance set, pick the snuggest pair that still twists.
4. Measure your STRÅLA hardware, fill the `// MEASURE` values in `config.scad`.
5. Render/export with `./validate_all.sh`, then slice and print.

## Validation

`./validate_all.sh` renders every part with OpenSCAD 2021.01, exports STL, and
checks each mesh for watertightness with trimesh. Results land in
`exports/reports/validation_results.json` and `validation_report.md`.

> Digital validation does not replace a real test print with the actual plug.
