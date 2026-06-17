# Measurement Guide

All values you must capture before printing the final adapters live in
`openscad/config.scad`, marked with `// MEASURE`. Use calipers (digital,
0.01 mm) and record each value, then update the config.

Print `strala_measurement_guide()` from `strala_holder.scad` — it engraves the
list of values you need to capture as a physical checklist.

## 1. The Schuko plug (already fixed in config, verify yours)

| Parameter            | Config value | How to measure |
|----------------------|--------------|----------------|
| `actual_plug_width`  | 41.8 mm      | widest flat across the body |
| `actual_plug_height` | 41.8 mm      | thickness across the body |
| `actual_plug_diagonal`| 41.8 mm     | corner-to-corner of body cross-section |
| `actual_plug_length` | 111 mm       | tip of pins to back of cable boot |

The bore is driven to **55 mm** regardless (the `plug_clear_passage_diameter`
floor), so even an oversized molded plug clears. If your plug's diagonal
exceeds 49 mm, increase `plug_clear_passage_diameter` and re-render — the echo
in `config.scad` will tell you whether you are still safe.

## 2. IKEA STRALA hardware (`// MEASURE`)

Measure your specific STRALA cord set — they vary by year and SKU.

| Config parameter                   | Placeholder | What it is |
|------------------------------------|-------------|------------|
| `strala_socket_outer_diameter`     | 30 mm       | OD of the plastic socket body the clamp grips |
| `strala_socket_total_length`       | 50 mm       | length of socket body from shoulder to top |
| `strala_shade_ring_outer_diameter` | 60 mm       | OD of the shade-retaining ring |
| `strala_shade_ring_inner_diameter` | 55 mm       | ID of that ring |
| `strala_thread_outer_diameter`     | 26 mm       | OD of the threaded collar (if present) |
| `strala_thread_length`             | 15 mm       | engaged length of that thread |
| `strala_cable_diameter`            | 6 mm        | OD of the cord jacket |

### Tips
- Measure the socket OD at three points (top, middle, shoulder) and use the
  **largest** for `strala_socket_outer_diameter`.
- For threads, measure the **major** (crest) diameter.
- Test the captured socket OD with `strala_fit_test_ring()` before committing.

## 3. Verifying the plug passage on a print

Print `passage_test_ring_55mm()` and `plug_gauge_set()`. Push your real plug
through the 55 mm gauge. If it binds, the plug is out of spec — bump
`plug_clear_passage_diameter` to 56–58 mm and re-export all modules.
