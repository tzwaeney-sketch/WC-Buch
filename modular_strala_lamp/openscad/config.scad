// ============================================================
// MODULAR STRÅLA LAMP — CENTRAL CONFIGURATION
// ============================================================
// All dimensions in mm. Edit here; everything else updates.

// --- Plug clearance (CRITICAL — do not reduce) ---
actual_plug_width     = 41.8;
actual_plug_height    = 41.8;
actual_plug_diagonal  = 41.8;
actual_plug_length    = 111.0;
plug_passage_clearance = 3.0;
plug_clear_passage_diameter = 60.0;

calculated_plug_passage = max(actual_plug_width, actual_plug_height, actual_plug_diagonal)
                          + 2 * plug_passage_clearance;  // = 47.8

final_plug_passage = max(calculated_plug_passage, plug_clear_passage_diameter); // = 60.0

// Assertions
assert(final_plug_passage >= plug_clear_passage_diameter,
       "ERROR: final_plug_passage below required minimum");

// Derived passage aliases (all modules use these)
bayonet_inner_diameter      = final_plug_passage;
base_passage_diameter       = final_plug_passage;
module_passage_diameter     = final_plug_passage;
top_cap_passage_diameter    = final_plug_passage;
calibration_passage_diameter = final_plug_passage;

echo("final_plug_passage =", final_plug_passage, "mm  [required >=", plug_clear_passage_diameter, "]");

// --- FDM print parameters (Bambu Lab P2S, 0.4mm nozzle) ---
nozzle_diameter   = 0.4;
layer_height      = 0.20;
line_width        = 0.42;

minimum_wall      = 1.68;   // 4 × line_width
structural_wall   = 2.52;   // 6 × line_width
reinforced_wall   = 3.36;   // 8 × line_width
base_wall         = 3.36;

general_clearance      = 0.25;
bayonet_radial_clearance = 0.30;
bayonet_axial_clearance  = 0.25;

assert(structural_wall >= minimum_wall, "ERROR: structural_wall below minimum_wall");

// --- Bayonet geometry (derived from plug passage) ---
bayonet_lug_count      = 3;
bayonet_lock_angle     = 25;      // degrees of rotation to lock
bayonet_working_depth  = 4.0;    // axial depth of lug pocket
bayonet_lug_height     = 2.4;    // lug thickness (axial)
bayonet_lug_radial_depth = 3.2;  // lug sticks this far into wall
bayonet_core_wall      = 3.0;    // wall between bore and lug inner face

// Derived radii
bayonet_bore_radius           = final_plug_passage / 2;             // 30.0
bayonet_core_outer_radius     = bayonet_bore_radius + bayonet_core_wall; // 33.0
male_lug_inner_radius         = bayonet_core_outer_radius;           // 33.0
male_lug_outer_radius         = male_lug_inner_radius + bayonet_lug_radial_depth; // 36.2
bayonet_interface_outer_radius = male_lug_outer_radius + bayonet_core_wall; // 39.2
bayonet_interface_outer_diameter = 2 * bayonet_interface_outer_radius;  // 78.4

// Female channel (slightly larger for clearance)
female_channel_inner_radius = male_lug_inner_radius - bayonet_radial_clearance; // 32.7
female_channel_outer_radius = male_lug_outer_radius + bayonet_radial_clearance; // 36.5
female_channel_height       = bayonet_lug_height + bayonet_axial_clearance;      // 2.65

assert(female_channel_inner_radius <= male_lug_inner_radius - bayonet_radial_clearance + 0.001);
assert(female_channel_outer_radius >= male_lug_outer_radius + bayonet_radial_clearance - 0.001);
assert(female_channel_height >= bayonet_lug_height + bayonet_axial_clearance - 0.001);

// --- Module geometry ---
minimum_module_outer_diameter = bayonet_interface_outer_diameter + 2 * structural_wall;
module_outer_diameter_typical = 105;  // main modules
module_outer_diameter_narrow  = ceil(bayonet_interface_outer_diameter + 2 * reinforced_wall); // ~86mm

// --- Lamp base ---
base_outer_diameter   = 220;
base_total_height     = 45;
base_bottom_thickness = 5;
base_outer_wall       = base_wall;

// --- STRÅLA adapter (MEASURE with real lamp) ---
strala_socket_outer_diameter   = 30;   // MEASURE
strala_socket_total_length     = 50;   // MEASURE
strala_shade_ring_outer_diameter = 60; // MEASURE
strala_shade_ring_inner_diameter = 55; // MEASURE
strala_thread_outer_diameter   = 26;   // MEASURE
strala_thread_length           = 15;   // MEASURE
strala_cable_diameter          = 6;    // MEASURE

// --- Lamp shades ---
shade_height          = 200;
shade_bottom_diameter = 250;
shade_top_diameter    = 110;
shade_wall            = 1.2;
shade_rib_count       = 48;
shade_rib_depth       = 1.5;
shade_ventilation_gap = 15;
shade_mount_diameter  = bayonet_interface_outer_diameter + 4;

// --- Body height target ---
lamp_body_target_height  = 600;
lamp_body_minimum_height = 570;
lamp_body_maximum_height = 630;

// --- Render quality ---
$fn = 64;

echo("=== CONFIGURATION SUMMARY ===");
echo("Plug passage:", final_plug_passage, "mm");
echo("Bayonet inner:", bayonet_inner_diameter, "mm");
echo("Bayonet interface OD:", bayonet_interface_outer_diameter, "mm");
echo("Min module OD:", minimum_module_outer_diameter, "mm");
echo("Typical module OD:", module_outer_diameter_typical, "mm");
echo("Base OD:", base_outer_diameter, "mm");
