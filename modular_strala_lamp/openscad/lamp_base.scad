// =====================================================================
// lamp_base.scad - The weighted base of the lamp system
// =====================================================================
include <config.scad>;
include <bayonet_system.scad>;
include <cable_passage.scad>;

// ---------------------------------------------------------------------
// Full base body. 180mm OD, 32mm tall, 55mm central passage,
// rear side cable exit, separate weight chamber, 4 foot recesses,
// male bayonet on top. Bottom plate is a separate part.
// ---------------------------------------------------------------------
module lamp_base() {
    od   = base_outer_diameter;
    h    = base_total_height;
    bore = base_passage_diameter;          // 55mm clear passage
    wall = base_outer_wall;                 // 3.4mm
    top_thk = base_wall;                    // structural top deck

    difference() {
        union() {
            // Outer shell
            difference() {
                cylinder(h = h, d = od, $fn = fn_large_bore);
                // Hollow interior (leaving top deck and walls)
                translate([0, 0, base_bottom_thickness])
                    cylinder(h = h, d = od - 2 * wall, $fn = fn_large_bore);
            }
            // Central passage tube spanning full height
            cylinder(h = h, d = bore + 2 * passage_wall, $fn = fn_large_bore);
            // Top deck closing the cavity around the passage tube
            translate([0, 0, h - top_thk])
                cylinder(h = top_thk, d = od - 2 * wall, $fn = fn_large_bore);
            // Weight chamber walls (an annular ring inside, separate from
            // the cable channel). Sits between passage tube and outer wall.
            difference() {
                cylinder(h = h - top_thk, d = od - 2 * wall - 6, $fn = fn_large_bore);
                translate([0, 0, -1])
                    cylinder(h = h + 2, d = od - 2 * wall - 6 - 2 * structural_wall,
                             $fn = fn_large_bore);
            }
            // Male bayonet on top
            translate([0, 0, h])
                bayonet_male(h = bayonet_working_depth);
        }

        // Clear central bore through everything
        translate([0, 0, -1])
            cylinder(h = h + bayonet_working_depth + 2, d = bore, $fn = fn_large_bore);

        // Rear side cable exit (smooth radius), enters the central tube
        translate([0, 0, h/2])
            rotate([0, 90, 0])
                hull() {
                    cylinder(h = od, d = 12, $fn = 48);
                    translate([0, 8, 0]) cylinder(h = od, d = 12, $fn = 48);
                }

        // 4x rubber foot recesses on the bottom (10mm dia, 2mm deep)
        for (i = [0:3])
            rotate([0, 0, 45 + i * 90])
                translate([od/2 - 22, 0, -0.01])
                    cylinder(h = 2, d = 14, $fn = 40);

        // Inner chamfer at the bore mouths
        _inner_chamfer(bore, h);
        translate([0,0,h + bayonet_working_depth]) mirror([0,0,1])
            _inner_chamfer(bore, h);

        // 3x M3 screw bosses for the bottom plate (clearance holes)
        for (i = [0:2])
            rotate([0, 0, i * 120])
                translate([od/2 - 14, 0, -0.01])
                    cylinder(h = 8, d = 2.8, $fn = 24);
    }
}

// ---------------------------------------------------------------------
// Bottom plate: closes the base, has a cable slot, 3x M3 counterbores.
// ---------------------------------------------------------------------
module lamp_base_bottom_plate() {
    od = base_outer_diameter - 2 * base_outer_wall - general_clearance;
    t  = base_bottom_thickness;
    difference() {
        cylinder(h = t, d = od, $fn = fn_large_bore);
        // Central clearance for passage tube
        translate([0, 0, -1])
            cylinder(h = t + 2, d = base_passage_diameter + 2 * passage_wall
                     + general_clearance, $fn = fn_large_bore);
        // Cable slot toward rear
        translate([od/2 - 20, -6, -1])
            cube([24, 12, t + 2]);
        // 3x M3 counterbored holes
        for (i = [0:2])
            rotate([0, 0, i * 120])
                translate([od/2 - 12, 0, -1]) {
                    cylinder(h = t + 2, d = 3.4, $fn = 24);   // shaft
                    translate([0, 0, t - 2.5])
                        cylinder(h = 3, d = 6.5, $fn = 24);   // head counterbore
                }
    }
}

// ---------------------------------------------------------------------
// Steel-plate weight insert: an annular disc that drops into the
// weight chamber. (Print as a template / or use for a cast/steel ring.)
// ---------------------------------------------------------------------
module lamp_base_weight_insert() {
    od = base_outer_diameter - 2 * base_outer_wall - 6 - general_clearance;
    id = base_passage_diameter + 2 * passage_wall + 4;
    t  = base_total_height - base_bottom_thickness - base_wall - 2;
    difference() {
        cylinder(h = t, d = od, $fn = fn_large_bore);
        translate([0, 0, -1])
            cylinder(h = t + 2, d = id, $fn = fn_large_bore);
    }
}

// ---------------------------------------------------------------------
// Cable strain relief insert: sits in the side exit, smooth 8-10mm bore.
// ---------------------------------------------------------------------
module cable_strain_relief_insert() {
    outer = 12 - general_clearance;
    len = 16;
    difference() {
        union() {
            cylinder(h = len, d = outer, $fn = 48);
            translate([0, 0, len - 2])
                cylinder(h = 2, d = outer + 4, $fn = 48);  // retaining flange
        }
        translate([0, 0, -1])
            cylinder(h = len + 4, d = 9, $fn = 48);        // smooth 9mm bore
        // Rounded mouth
        translate([0, 0, len + 2]) mirror([0,0,1])
            rotate_extrude($fn = 48) translate([4.5, 0]) circle(r = 1.2, $fn = 24);
    }
}

// Preview
// lamp_base();
