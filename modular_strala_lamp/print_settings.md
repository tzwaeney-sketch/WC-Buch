# Print Settings — Bambu Lab P2S

These settings target a Bambu Lab P2S (0.4 mm nozzle) and the wall multiples
used throughout the SCAD files (multiples of `line_width = 0.42 mm`).

## Global

| Setting | Value |
|---------|-------|
| Nozzle | 0.4 mm |
| Layer height | 0.20 mm |
| First layer height | 0.25 mm |
| Line width | 0.42 mm |
| Wall loops | 4 (gives the 1.68 mm `minimum_wall`) |
| Top/bottom layers | 4 / 4 |
| Infill | 15 % gyroid (modules), 25 % (base) |
| Seam | aligned / rear |

Because walls are exact multiples of 0.42 mm (1.68 / 2.10 / 2.52 / 2.94 /
3.36), the slicer fills them with whole perimeters — no gap fill, clean bores.

## Material profiles

| Part | Material | Nozzle temp | Bed | Notes |
|------|----------|-------------|-----|-------|
| Base, lower modules | PLA | 210 °C | 55 °C | fine away from bulb |
| Modules near bulb, top cap | PETG | 240 °C | 75 °C | heat resistance |
| Top cap / shade (hot builds) | ASA | 250 °C | 95 °C | enclosure + glue stick |
| Strain relief | PETG | 240 °C | 75 °C | needs some grip/flex |

## Orientation & supports

- **All parts are designed to print flat on the bed with the bayonet axis
  vertical.** Bores print as vertical holes — no bridging across the 55 mm bore.
- Bayonet lugs are self-supporting (short overhangs < 4 mm). No supports needed
  for `bayonet_male`/`bayonet_female`.
- Shades: print mouth-down (mounting ring on the bed). Thin walls (1.2 mm)
  print as 3 perimeters with `line_width` 0.42 — vase mode optional for the
  smooth shades (`shade_cylinder`, `shade_frustum`).
- `lamp_base`: print as-is, cavity up. The side cable exit may need a few
  support lines depending on overhang angle — enable "support on build plate
  only" if your slicer flags it.

## Tolerance tuning

1. Print `bayonet_tolerance_set` first.
2. Find the clearance that gives a firm twist-lock with no slop.
3. Set `bayonet_radial_clearance` in `config.scad` to that value (default 0.30).
4. Re-export modules.

## Quality flags (CLI)

```
openscad -o part.stl --enable=fast-csg -D '$fn=128' _tmp.scad
```

Use `$fn = 128` for final renders of large bores; 64 is fine for previews.

## Strength notes
- Bottom plate and base get 25 % infill for ballast stiffness.
- Decorative modules can go lower (10–15 %); they carry only the stack above
  via the bayonet ring, which is solid-walled regardless of infill.
