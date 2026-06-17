# Assembly Guide

## Before you start
- Complete `measurements.md` and update `config.scad`.
- Print and validate all parts in `calibration_parts.scad`.
- Have an IKEA STRALA cord set with an attached Schuko plug.

## Parts per lamp (typical `config_soft_round`)
- 1x `lamp_base`
- 1x `lamp_base_bottom_plate` + 3x M3x10 screws
- 1x `lamp_base_weight_insert` (or a steel ring of matching dimensions)
- 1x `cable_strain_relief_insert`
- N decorative modules (e.g. sphere + disc + ring)
- 1x `strala_top_cap`
- 1x shade + its integral `shade_mounting_ring`
- 4x stick-on rubber feet

## Step 1 — Route the cable (the whole point)
1. Lay the STRALA cord flat, plug attached.
2. Feed the **plug end** up through the base passage, then through each module
   in stacking order, then through the top cap.
3. Because every bore is >= 55 mm, the plug passes through with no rewiring.
   Leave the plug hanging out the bottom; the socket end stays at the top.

## Step 2 — Build the base
1. Drop the weight insert into the weight chamber.
2. Press the `cable_strain_relief_insert` into the rear side exit.
3. Route the cable out the side exit through the strain relief.
4. Fit the `lamp_base_bottom_plate`, aligning the cable slot to the rear.
5. Secure with 3x M3 screws (counterbored from below).
6. Apply 4x rubber feet to the foot recesses.

## Step 3 — Stack the modules (bayonet)
For each joint:
1. Align the three male lugs with the three entry slots of the female above.
2. Push down `bayonet_working_depth` (~4 mm) until seated.
3. **Twist 25°** until it stops — this locks the lugs in the channel.
4. To remove later: twist back 25°, lift.

Stack overlap is `bayonet_working_depth`, already accounted for in the preview.

## Step 4 — Top cap + STRALA socket
1. Lock the `strala_top_cap` onto the top module via its female bayonet.
2. Seat the STRALA socket body into the holder bore.
3. If using a clamp adapter, fit `strala_clamp_adapter` and tighten its M3
   clamp screws onto the socket body.
4. Route any slack cable through the holder's side-entry relief.

## Step 5 — Shade
1. Slip the shade's integral `shade_mounting_ring` over the top cap / top
   module interface.
2. Confirm the ventilation gaps are open (do not block them — see safety).

## Step 6 — Final check
- Tug-test every bayonet joint (twist-locked, not just pushed).
- Confirm the bulb does not touch any printed wall.
- Plug in and verify the strain relief holds the cable.
