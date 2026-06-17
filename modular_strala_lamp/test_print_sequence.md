# Test Print Sequence

Print in this order. Do not advance until the current step passes.

## Phase 1 — Critical clearance

1. `passage_test_ring(60)` — push the **real plug** through. Must pass freely.
2. `long_tunnel_test` (60 mm × 65 mm) — confirm the plug clears a deep bore.

> Only after both pass may you state: "Realer Steckerdurchgang erfolgreich
> geprüft." Until then the project is only digitally validated.

## Phase 2 — Bayonet fit

3. `bayonet_tolerance_pair(0.20)` … `(0.40)` — print all five.
4. `bayonet_snap_test` — confirm the chosen clearance twists 25° and locks.
5. Record the winning clearance; set `bayonet_radial_clearance` in config.

## Phase 3 — Base systems

6. `cable_exit_test` — confirm cable routes through channel + side exit.
7. `shade_wall_test` — pick the thinnest wall that prints cleanly.

## Phase 4 — STRÅLA fit

8. `strala_fit_test` — measure real socket, set
   `strala_socket_outer_diameter`.

## Phase 5 — Full parts

9. `lamp_base` + `lamp_base_bottom_plate` + `cable_exit_grommet`.
10. One decorative module of choice.
11. `mod_top_cap` + `strala_split_clamp_left/right`.
12. One shade.

## Phase 6 — Assembly & stability

13. Follow `assembly.md`.
14. Run the stability check in `stability_report.md` with the largest shade.
