# Print Settings — Bambu Lab P2S

| Setting | Value |
|---------|-------|
| Nozzle | 0.4 mm |
| Layer height | 0.20 mm |
| Line width | 0.42 mm |
| Walls (perimeters) | 4 (minimum), 6 (structural), 8 (reinforced/base) |
| Top/bottom layers | 5 |
| Infill | 15 % gyroid (modules), 25 % (base) |

## Material by part

| Part | Material | Nozzle temp | Bed temp | Notes |
|------|----------|-------------|----------|-------|
| Base, lower modules | PLA | 210 °C | 55 °C | fine away from bulb |
| Top cap, shade | PETG / ASA | 250 / 260 °C | 80 / 90 °C | bulb heat |
| Grommet | TPU / PETG | 230 °C | 60 °C | flexible seal |

## Orientation

- Print all bores **vertical** so the 60 mm hole forms as a clean vertical
  cylinder — no bridging across the passage.
- Bayonet lugs print without support thanks to their 2.4 mm axial height and
  shallow angle.
- Shades print upright; the integral mounting ring is the build-plate contact.

## Tolerances

- Bayonet radial clearance: 0.30 mm (tune with the tolerance set).
- General clearance: 0.25 mm.
- If joints are too tight, print the next-looser tolerance pair, do not sand the
  bore (it must stay >= 60 mm).
