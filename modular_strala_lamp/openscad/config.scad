// =====================================================================
// config.scad - Central configuration for Modular STRALA Lamp System
// =====================================================================
// CRITICAL REQUIREMENT:
//   A full Schuko plug (55mm clear passage diameter) must pass through
//   EVERY part of the system without disassembly.
// =====================================================================

// ---------------------------------------------------------------------
// Plug clearance - CRITICAL
// ---------------------------------------------------------------------
actual_plug_width      = 41.8;
actual_plug_height     = 41.8;
actual_plug_length     = 111;
actual_plug_diagonal   = 41.8;
plug_passage_clearance = 3.0;
plug_clear_passage_diameter = 55.0;

// ---------------------------------------------------------------------
// Derived passage
// ---------------------------------------------------------------------
calculated_plug_passage =
    max(actual_plug_width, actual_plug_height, actual_plug_diagonal)
    + 2 * plug_passage_clearance;

final_plug_passage = max(calculated_plug_passage, plug_clear_passage_diameter);

// Assertion / warning: the final passage must never be smaller than the
// mandated clear passage diameter.
if (final_plug_passage < plug_clear_passage_diameter) {
    echo("=====================================================");
    echo("WARNING: final_plug_passage is SMALLER than the mandated");
    echo("clear passage diameter! The plug will NOT fit.");
    echo(str("  final_plug_passage        = ", final_plug_passage));
    echo(str("  plug_clear_passage_diameter = ", plug_clear_passage_diameter));
    echo("=====================================================");
} else {
    echo(str("OK: final_plug_passage = ", final_plug_passage,
             " mm (>= ", plug_clear_passage_diameter, " mm required)"));
}
// Hard assert (uncomment to make rendering fail on violation):
// assert(final_plug_passage >= plug_clear_passage_diameter,
//        "final_plug_passage must be >= plug_clear_passage_diameter");

// ---------------------------------------------------------------------
// FDM parameters
// ---------------------------------------------------------------------
nozzle_diameter   = 0.4;
layer_height      = 0.20;
line_width        = 0.42;
general_clearance = 0.25;
bayonet_radial_clearance = 0.30;
bayonet_axial_clearance  = 0.25;
minimum_wall   = 1.68;   // 4 lines
structural_wall = 2.52;  // 6 lines
base_wall      = 3.36;   // 8 lines

// ---------------------------------------------------------------------
// Bayonet system
// ---------------------------------------------------------------------
bayonet_inner_diameter           = 55;  // = final_plug_passage
bayonet_interface_outer_diameter = 74;
minimum_module_outer_diameter    = 78;
passage_wall            = 2.5;
bayonet_working_depth   = 4.0;
bayonet_lug_radial_depth = 3.5;
bayonet_outer_wall      = 3.0;
bayonet_lug_count       = 3;
bayonet_lock_angle      = 25;   // degrees of twist to lock
bayonet_lug_angular_width = 30; // degrees each lug spans

// ---------------------------------------------------------------------
// Lamp base
// ---------------------------------------------------------------------
base_outer_diameter   = 180;
base_total_height     = 32;
base_bottom_thickness = 4;
base_outer_wall       = 3.4;
base_passage_diameter = 55;

// ---------------------------------------------------------------------
// Modules
// ---------------------------------------------------------------------
module_height_min            = 35;
module_height_max            = 90;
module_outer_diameter_min    = 78;
module_outer_diameter_typical = 95;

// ---------------------------------------------------------------------
// Shades
// ---------------------------------------------------------------------
shade_height          = 150;
shade_bottom_diameter = 210;
shade_top_diameter    = 105;
shade_wall            = 1.2;
shade_rib_count       = 48;
shade_rib_depth       = 1.5;
shade_ventilation_gap = 12;
shade_mount_diameter  = 95;  // parametric mount interface for all shades

// ---------------------------------------------------------------------
// STRALA holder - MEASURE markers
// ---------------------------------------------------------------------
strala_socket_outer_diameter     = 30;  // MEASURE
strala_socket_total_length       = 50;  // MEASURE
strala_shade_ring_outer_diameter = 60;  // MEASURE
strala_shade_ring_inner_diameter = 55;  // MEASURE
strala_thread_outer_diameter     = 26;  // MEASURE
strala_thread_length             = 15;  // MEASURE
strala_cable_diameter            = 6;   // MEASURE

// ---------------------------------------------------------------------
// Quality / preview settings
// ---------------------------------------------------------------------
$fn = 64;            // default circle resolution
fn_large_bore = 128; // resolution for large 55mm bores
inner_chamfer = 2.0; // minimum chamfer on inner edges
inner_radius  = 3.0; // minimum radius on inner edges

// Show plug clearance test overlay
show_plug_clearance_test = false;
