# Measurement Guide

All values you must capture before printing the final adapters live in
`openscad/config.scad`, marked with `// MEASURE`. Use digital calipers
(0.01 mm) and record each value, then update the config.

## 1. The Schuko plug (already fixed in config, verify yours)

| Parameter            | Config value | How to measure |
|----------------------|--------------|----------------|
| `actual_plug_width`  | 41.8 mm      | widest flat across the body |
| `actual_plug_height` | 41.8 mm      | thickness across the body |
| `actual_plug_diagonal`| 41.8 mm     | corner-to-corner of body cross-section |
| `actual_plug_length` | 111 mm       | tip of pins to back of cable boot |

The bore is driven to **60 mm** regardless (the `plug_clear_passage_diameter`
floor), so even an oversized molded plug clears. If your plug's diagonal
exceeds 54 mm, increase `plug_clear_passage_diameter` and re-render — the echo
in `config.scad` will tell you whether you are still safe.

## 2. IKEA STRÅLA hardware (`// MEASURE`)

Measure your specific STRÅLA cord set — they vary by year and SKU.

| Config parameter                   | Placeholder | What it is |
|------------------------------------|-------------|------------|
| `strala_socket_outer_diameter`     | 30 mm       | OD of the plastic socket body the clamp grips |
| `strala_socket_total_length`       | 50 mm       | length of the socket body |
| `strala_shade_ring_outer_diameter` | 60 mm       | OD of the shade retaining ring |
| `strala_shade_ring_inner_diameter` | 55 mm       | ID of that ring |
| `strala_thread_outer_diameter`     | 26 mm       | thread OD if present |
| `strala_thread_length`             | 15 mm       | thread length |
| `strala_cable_diameter`            | 6 mm        | OD of the cable jacket |

## 3. Verifying the passage

Print `passage_test_ring(60)` from `calibration_parts.scad`. Push your real
plug through the 60 mm gauge. It must pass freely. If it binds, the plug is out
of spec — bump `plug_clear_passage_diameter` and re-render.

## 4. Verifying the STRÅLA clamp fit

Print `strala_fit_test()` from `strala_holder.scad`. It produces five rings at
+0.0 / +0.5 / +1.0 / +1.5 / +2.0 mm over the nominal socket OD. Pick the ring
that slides on snugly, then set `strala_socket_outer_diameter` accordingly.
