// =====================================================================
// export_all.scad - Export reference (comments only)
// =====================================================================
// This file documents how to export every printable part as STL.
// It contains no geometry on purpose.
//
// The canonical, automated exporter is ../validate_all.sh — it renders
// every part with OpenSCAD, exports STL to ../exports/stl/, and validates
// each mesh with trimesh. Use that for a full build.
//
// Manual single-part export (Method A, most robust):
//   export OPENSCADPATH=$PWD          # so include <config.scad> resolves
//   echo 'include <lamp_base.scad>; lamp_base();' > _tmp.scad
//   openscad -o lamp_base.stl _tmp.scad
//
// NOTE: every library file's trailing demo call is wrapped in
//   if ($preview) <demo>();
// so it renders only in the GUI and is skipped during -o STL export.
// That is why a wrapper that includes the file and calls one module
// exports exactly that one module, with no contamination.
//
// ---------------------------------------------------------------------
// Full part list  (FILE  ->  MODULES)
// ---------------------------------------------------------------------
// bayonet_system.scad:
//   bayonet_male, bayonet_female, bayonet_pair, bayonet_passage_ring,
//   bayonet_section_view, bayonet_tolerance_pair(clearance)
//
// cable_passage.scad:
//   cable_guide_channel, plug_test_body, plug_clearance_test_body,
//   cable_exit_fitting
//
// lamp_base.scad:
//   lamp_base, lamp_base_bottom_plate, lamp_base_weight_insert,
//   cable_exit_grommet
//
// strala_holder.scad:
//   strala_fit_test, strala_split_clamp_left, strala_split_clamp_right
//
// round_modules.scad:
//   mod_sphere, mod_oblate_sphere, mod_double_sphere, mod_soft_cylinder,
//   mod_disc, mod_ring_module
//
// geometric_modules.scad:
//   mod_cube_rounded, mod_hexagon, mod_diamond_faceted, mod_frustum,
//   mod_triangle_rounded, mod_stepped_geometric
//
// organic_modules.scad:
//   mod_teardrop, mod_vase, mod_pumpkin, mod_wave, mod_organic_diamond,
//   mod_asymmetric_soft, mod_narrow_shadow_ring, mod_narrow_ribbed_ring
//
// utility_modules.scad:
//   mod_neutral_extension, mod_short_spacer, mod_top_cap, mod_transition
//
// lamp_shades.scad:
//   shade_frustum, shade_cylinder, shade_bell, shade_mushroom, shade_globe,
//   shade_vertical_ribs, shade_horizontal_ribs, shade_faceted,
//   shade_organic_curve, shade_perforated, shade_mounting_ring
//
// calibration_parts.scad:
//   passage_test_ring(d), long_tunnel_test, bayonet_snap_test,
//   shade_wall_test, cable_exit_test
//
// passage_variants.scad:
//   passage_test_ring(d), passage_variants
//
// assembly_preview.scad:
//   config_soft_round, config_geometric, config_organic, config_minimal,
//   config_mixed
// =====================================================================
