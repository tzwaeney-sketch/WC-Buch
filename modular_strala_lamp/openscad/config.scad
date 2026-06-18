// ============================================================
// config.scad — Modular STRALA Lamp System V2
// All global parameters. Included by every other v2 file.
// All dimensions in mm.
// ============================================================

// ---- Plug passage (NEVER reduce) ----
final_plug_passage = 60.0;
bore_r = final_plug_passage / 2;   // 30.0
assert(bore_r * 2 >= 60, "Bore diameter must be >= 60mm (plug passage)");

// ---- FDM print parameters (Bambu P2S, 0.4mm nozzle) ----
nozzle_d = 0.4;
lh = 0.20;
lw = 0.42;
wall_min  = 1.68;   // 4 x lw
wall_str  = 2.52;   // 6 x lw
wall_rein = 3.36;   // 8 x lw
clearance = 0.30;   // default (between PLA 0.25 and PETG 0.35)
EPS = 0.01;

// ---- Bayonet geometry (mathematically defined) ----
bay_core_wall   = 3.5;
bay_lug_inner_r = bore_r + bay_core_wall;          // 33.5
bay_lug_depth   = 3.5;
bay_lug_outer_r = bay_lug_inner_r + bay_lug_depth; // 37.0
bay_iface_wall  = 3.0;
bay_iface_r     = bay_lug_outer_r + bay_iface_wall;// 40.0
bay_iface_d     = bay_iface_r * 2;                 // 80.0

bay_n         = 3;    // number of lugs
bay_lug_arc   = 22;   // lug angular width (deg)
bay_entry_arc = 30;   // entry slot width (deg) — wider than lug+tol
bay_lock_arc  = 25;   // rotation to lock (deg)
bay_lug_h     = 2.8;  // lug axial thickness (mm)
bay_depth     = 5.0;  // total bayonet zone height (mm)

// ---- Snap geometry ----
snap_ramp_deg = 4;    // degrees of ramp at end of lock groove
snap_step     = 0.5;  // mm depth of snap well behind ramp

// ---- Module sizing ----
mod_typical_d = 105;                      // typical outer diameter
mod_narrow_d  = 88;                       // narrow accent modules min OD
mod_min_d     = bay_iface_d + 2*wall_str; // absolute minimum OD (~85)

// ---- Base ----
base_d   = 220;
base_h   = 45;
base_bot = 5;

// ---- STRALA fixture (measured) ----
strala_thread_d    = 26;
strala_shoulder_d  = 38;
strala_ret_ring_od = 36;
strala_cable_d     = 6;
strala_mount_clearance = 0.6;
strala_mount_hole_d = strala_thread_d + strala_mount_clearance;

// ---- Shade ----
shade_h     = 200;
shade_bot_d = 240;
shade_top_d = 110;
shade_wall_t= 1.6;
shade_vent  = 15;

$fn = 64;
