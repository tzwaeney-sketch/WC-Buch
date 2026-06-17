# Bambu Studio Guide

How to slice the STRÅLA lamp parts in Bambu Studio for the P2S.

## 1. Import

- Import the STL files from `exports/stl/<category>/`.
- One part per plate for large modules; calibration parts can share a plate.

## 2. Profile

- Printer: Bambu Lab P2S, 0.4 mm nozzle.
- Process: 0.20 mm Standard, then override:
  - Wall loops: 4 (modules), 6–8 (base/top cap).
  - Top/bottom shells: 5 layers.
  - Sparse infill: 15 % gyroid (modules), 25 % (base).

## 3. Orientation

- Place every bored part with the bore axis **vertical**.
- Base sits flange-down; modules sit female-bayonet-down.
- Shades sit mounting-ring-down.

## 4. Supports

- Most parts print support-free.
- The STRÅLA split clamp halves: enable support **on build plate only** for the
  screw bosses if they overhang.

## 5. Material slots (AMS)

| Slot | Filament | Used for |
|------|----------|----------|
| 1 | PLA | base, lower modules |
| 2 | PETG | top cap, shade, grommet |
| 3 | ASA | high-heat shade variant |

## 6. Before printing the whole lamp

Slice and print the calibration plate first. Only proceed to full modules once
`passage_test_ring(60)` passes the real plug and a bayonet tolerance pair locks
cleanly.

## 7. Flow / dimensional accuracy

Run a flow-ratio calibration; bore diameter accuracy is critical for the 60 mm
clearance. Verify a printed `passage_test_ring(60)` measures 60.0 mm ± 0.2 mm.
