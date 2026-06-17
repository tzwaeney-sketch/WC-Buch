# Modular STRALA Lamp System

A fully parametric, 3D-printable modular table lamp system built around IKEA
STRALA cord/socket hardware. Decorative modules stack via a twist-lock
**bayonet** interface so you can build endless lamp shapes from a shared kit.

## The one rule that drives everything

> **A complete Schuko plug must pass through every single part — without
> disassembling anything.**

This means the central clear bore is **never smaller than 55 mm** anywhere in
the system. You can thread an already-wired cable (plug attached) up through the
base, every module, the top cap, and out to the STRALA socket. No cutting the
cable, no rewiring.

The clearance math lives in `openscad/config.scad`:

```
calculated_plug_passage = max(width, height, diagonal) + 2 * clearance
                        = max(41.8, 41.8, 41.8) + 2 * 3.0 = 47.8 mm
final_plug_passage      = max(47.8, 55.0) = 55.0 mm   <-- governs all bores
```

A render-time `echo`/assert in `config.scad` warns if this ever drops below
55 mm.

## Architecture

```
modular_strala_lamp/
├── README.md            <- this file
├── measurements.md      <- how to measure your STRALA + plug
├── assembly.md          <- step-by-step build
├── safety.md            <- electrical / thermal safety
├── bom.md               <- bill of materials
├── print_settings.md    <- Bambu Lab P2S profile
└── openscad/
    ├── config.scad            central parameters + derived values
    ├── bayonet_system.scad    male/female twist-lock interface
    ├── cable_passage.scad     channels, plug test bodies, exits
    ├── lamp_base.scad         weighted base + bottom plate + inserts
    ├── strala_holder.scad     IKEA STRALA adapters (MEASURE markers)
    ├── round_modules.scad     spheres, discs, rings, soft cylinders
    ├── geometric_modules.scad cubes, hexes, diamonds, frustums
    ├── organic_modules.scad   teardrops, vases, pumpkins, waves
    ├── lamp_shades.scad       11 shades + structural mounting ring
    ├── calibration_parts.scad gauges + tolerance tests (print FIRST)
    ├── assembly_preview.scad  5 stacked example configurations
    └── export_all.scad        CLI export reference (comments only)
```

## The bayonet interface

Every module exposes a **female** bayonet at the bottom and a **male** bayonet
at the top. Three lugs and a 25° twist lock the joint. Critically, the lugs sit
**in the wall** between the 55 mm bore and the 74 mm interface OD — they never
intrude into the clear passage. Tune the fit with the parts in
`calibration_parts.scad` before printing modules.

## How to use

1. Read `measurements.md` and measure your STRALA hardware and your plug.
2. Update the `// MEASURE` values in `config.scad`.
3. Print everything in `calibration_parts.scad` and dial in tolerances.
4. Pick a configuration in `assembly_preview.scad` (or design your own stack).
5. Export parts (see `export_all.scad`), print, and assemble per `assembly.md`.

## Rendering

Open `openscad/assembly_preview.scad` in OpenSCAD. It defaults to
`config_soft_round()`. Set `show_plug_clearance_test = true` in `config.scad`
to overlay a translucent 55 mm rod confirming the clear passage.

## License / disclaimer

Provided as-is. Mains electricity is dangerous — read `safety.md`.
