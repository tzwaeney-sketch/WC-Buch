// =====================================================================
// export_all.scad - Export reference (comments only)
// =====================================================================
// This file documents how to export every printable part as STL using
// the OpenSCAD command line. It contains no geometry on purpose.
//
// General pattern (OpenSCAD 2021.01+ supports -D module calls via a
// wrapper). Because OpenSCAD CLI exports the *top-level* geometry, the
// recommended approach is one of:
//
//   A) Create a tiny wrapper .scad that `include`s the source file and
//      calls the single module, then export that wrapper, OR
//   B) Use -D 'PART="name"' with a dispatcher (see bottom).
//
// ---------------------------------------------------------------------
// Method A example (recommended, most robust):
// ---------------------------------------------------------------------
//   echo 'include <lamp_base.scad>; lamp_base();' > _tmp.scad
//   openscad -o lamp_base.stl _tmp.scad
//
// ---------------------------------------------------------------------
// Full part list  (FILE  ->  MODULE)
// ---------------------------------------------------------------------
// bayonet_system.scad:
//   bayonet_male, bayonet_female, bayonet_passage_ring, bayonet_cross_section
//
// cable_passage.scad:
//   cable_guide_channel, plug_test_body, plug_clearance_test_body, cable_exit_fitting
//
// lamp_base.scad:
//   lamp_base, lamp_base_bottom_plate, lamp_base_weight_insert, cable_strain_relief_insert
//
// strala_holder.scad:
//   strala_clamp_adapter, strala_shade_ring_adapter, strala_top_cap,
//   strala_test_adapter, strala_measurement_guide
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
//   mod_teardrop, mod_vase, mod_asymmetric_soft, mod_pumpkin, mod_wave,
//   mod_organic_diamond
//
// lamp_shades.scad:
//   shade_frustum, shade_cylinder, shade_bell, shade_mushroom, shade_globe,
//   shade_vertical_ribs, shade_horizontal_ribs, shade_faceted,
//   shade_organic_curve, shade_perforated, shade_mounting_ring
//
// calibration_parts.scad:
//   plug_gauge_ring, plug_gauge_set, passage_test_ring_55mm,
//   bayonet_tolerance_test, bayonet_tolerance_set, strala_fit_test_ring,
//   cable_exit_test, shade_wall_test
//
// assembly_preview.scad:
//   config_soft_round, config_geometric, config_minimal, config_organic, config_mixed
//
// ---------------------------------------------------------------------
// Batch export script (bash):
// ---------------------------------------------------------------------
//   #!/usr/bin/env bash
//   set -e
//   declare -A PARTS=(
//     [lamp_base]=lamp_base.scad
//     [lamp_base_bottom_plate]=lamp_base.scad
//     [mod_sphere]=round_modules.scad
//     [shade_frustum]=lamp_shades.scad
//     [passage_test_ring_55mm]=calibration_parts.scad
//     # ...add the rest from the list above...
//   )
//   mkdir -p stl
//   for part in "${!PARTS[@]}"; do
//     file="${PARTS[$part]}"
//     echo "include <$file>; $part();" > _tmp.scad
//     openscad -o "stl/${part}.stl" _tmp.scad
//   done
//   rm -f _tmp.scad
//
// ---------------------------------------------------------------------
// Render quality flags for final STL:
//   openscad -o part.stl --enable=fast-csg \
//            -D '$fn=128' _tmp.scad
// =====================================================================
