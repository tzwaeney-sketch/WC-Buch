// =====================================================================
// lamp_shades.scad - Lamp shades (mount onto a top module / cap)
// =====================================================================
// Shades are thin-walled and attach to a stable mounting ring whose
// inner diameter = shade_mount_diameter. The thin shade wall is never
// load bearing; the ring carries the joint.
// =====================================================================
include <config.scad>

// ---------------------------------------------------------------------
// Mounting ring: stable structural ring all shades attach to.
// Sits over the top module; bore stays clear (>= 55mm).
// ---------------------------------------------------------------------
module shade_mounting_ring(mount_d = shade_mount_diameter) {
    h = 14;
    bore = max(final_plug_passage, mount_d - 2 * structural_wall);
    difference() {
        cylinder(h = h, d = mount_d + 2 * structural_wall, $fn = fn_large_bore);
        // Recess that slips over the top module
        translate([0, 0, 2])
            cylinder(h = h, d = mount_d + general_clearance, $fn = fn_large_bore);
        // Clear central bore
        translate([0, 0, -1])
            cylinder(h = h + 2, d = bore, $fn = fn_large_bore);
        // Ventilation gap notches
        for (i = [0:5])
            rotate([0, 0, i * 60])
                translate([mount_d/2, 0, h - shade_ventilation_gap/2])
                    cube([2 * structural_wall + 2, 6, shade_ventilation_gap], center = true);
    }
}

// Shared: attach a thin shade profile (2D points, rotate_extrude) onto
// the mounting ring. `profile` is a list of [r, z] points.
module _shade_from_profile(profile, mount_d = shade_mount_diameter) {
    union() {
        shade_mounting_ring(mount_d);
        translate([0, 0, 14])
            difference() {
                rotate_extrude($fn = 120) polygon(profile);
                // hollow it out by shade_wall
                rotate_extrude($fn = 120)
                    offset(delta = -shade_wall) polygon(profile);
            }
    }
}

// ---------------------------------------------------------------------
// Frustum (truncated cone) shade.
// ---------------------------------------------------------------------
module shade_frustum() {
    _shade_from_profile([
        [shade_mount_diameter/2, 0],
        [shade_bottom_diameter/2, 6],
        [shade_top_diameter/2, shade_height],
        [shade_top_diameter/2 - shade_wall, shade_height],
        [shade_bottom_diameter/2 - shade_wall, 6],
        [shade_mount_diameter/2 - shade_wall, 0],
    ]);
}

// ---------------------------------------------------------------------
// Straight cylinder shade.
// ---------------------------------------------------------------------
module shade_cylinder() {
    d = shade_bottom_diameter * 0.8;
    union() {
        shade_mounting_ring();
        translate([0, 0, 14])
            difference() {
                cylinder(h = shade_height, d = d, $fn = 120);
                translate([0, 0, -1])
                    cylinder(h = shade_height + 2, d = d - 2 * shade_wall, $fn = 120);
            }
    }
}

// ---------------------------------------------------------------------
// Bell / dome shade.
// ---------------------------------------------------------------------
module shade_bell() {
    pts = [ for (i = [0:24])
        let (a = 90 * i / 24,
             r = shade_bottom_diameter/2 * cos(a) * 0.6 + shade_top_diameter/2,
             z = shade_height * sin(a))
        [r, z] ];
    prof = concat(
        [[shade_mount_diameter/2, 0]],
        pts,
        [ for (i = [24:-1:0])
            let (a = 90 * i / 24,
                 r = shade_bottom_diameter/2 * cos(a) * 0.6 + shade_top_diameter/2,
                 z = shade_height * sin(a))
            [max(1, r - shade_wall), z] ],
        [[shade_mount_diameter/2 - shade_wall, 0]]
    );
    union() {
        shade_mounting_ring();
        translate([0, 0, 14]) rotate_extrude($fn = 120) polygon(prof);
    }
}

// ---------------------------------------------------------------------
// Mushroom cap shade.
// ---------------------------------------------------------------------
module shade_mushroom() {
    union() {
        shade_mounting_ring();
        translate([0, 0, 14])
            difference() {
                scale([1, 1, 0.55])
                    sphere(d = shade_bottom_diameter, $fn = 120);
                scale([1, 1, 0.55])
                    sphere(d = shade_bottom_diameter - 2 * shade_wall, $fn = 120);
                translate([0, 0, -shade_bottom_diameter])
                    cylinder(h = shade_bottom_diameter, d = shade_bottom_diameter + 2, $fn = 8);
            }
    }
}

// ---------------------------------------------------------------------
// Globe / sphere shade (with bottom opening).
// ---------------------------------------------------------------------
module shade_globe() {
    d = shade_bottom_diameter * 0.85;
    union() {
        shade_mounting_ring();
        translate([0, 0, 14 + d/2 - 10])
            difference() {
                sphere(d = d, $fn = 120);
                sphere(d = d - 2 * shade_wall, $fn = 120);
                // bottom opening for mounting
                translate([0, 0, -d/2])
                    cylinder(h = d/2, d = shade_mount_diameter + 6, $fn = 96);
            }
    }
}

// ---------------------------------------------------------------------
// Vertical ribs shade.
// ---------------------------------------------------------------------
module shade_vertical_ribs() {
    union() {
        shade_frustum();
        for (i = [0 : shade_rib_count - 1])
            rotate([0, 0, i * 360 / shade_rib_count])
                translate([shade_bottom_diameter/2 - 2, 0, 14])
                    rotate([0, 6, 0])
                        cube([shade_rib_depth, 2, shade_height]);
    }
}

// ---------------------------------------------------------------------
// Horizontal ribs shade.
// ---------------------------------------------------------------------
module shade_horizontal_ribs() {
    union() {
        shade_cylinder();
        d = shade_bottom_diameter * 0.8;
        for (z = [10 : 12 : shade_height - 10])
            translate([0, 0, 14 + z])
                rotate_extrude($fn = 120)
                    translate([d/2, 0]) circle(r = shade_rib_depth, $fn = 16);
    }
}

// ---------------------------------------------------------------------
// Faceted polygon shade.
// ---------------------------------------------------------------------
module shade_faceted() {
    sides = 10;
    union() {
        shade_mounting_ring();
        translate([0, 0, 14])
            difference() {
                cylinder(h = shade_height, d1 = shade_bottom_diameter,
                         d2 = shade_top_diameter, $fn = sides);
                translate([0, 0, -1])
                    cylinder(h = shade_height + 2,
                             d1 = shade_bottom_diameter - 2 * shade_wall,
                             d2 = shade_top_diameter - 2 * shade_wall, $fn = sides);
            }
    }
}

// ---------------------------------------------------------------------
// Organic S-curve shade.
// ---------------------------------------------------------------------
module shade_organic_curve() {
    pts = [ for (i = [0:30])
        let (t = i / 30,
             z = shade_height * t,
             r = shade_bottom_diameter/2
                 - (shade_bottom_diameter/2 - shade_top_diameter/2) * t
                 + 18 * sin(180 * t))
        [r, z] ];
    prof = concat(
        [[shade_mount_diameter/2, 0]],
        pts,
        [ for (i = [30:-1:0])
            let (t = i / 30,
                 z = shade_height * t,
                 r = shade_bottom_diameter/2
                     - (shade_bottom_diameter/2 - shade_top_diameter/2) * t
                     + 18 * sin(180 * t))
            [r - shade_wall, z] ],
        [[shade_mount_diameter/2 - shade_wall, 0]]
    );
    union() {
        shade_mounting_ring();
        translate([0, 0, 14]) rotate_extrude($fn = 120) polygon(prof);
    }
}

// ---------------------------------------------------------------------
// Perforated shade (circular hole pattern).
// ---------------------------------------------------------------------
module shade_perforated() {
    d1 = shade_bottom_diameter * 0.8;
    rows = 8; cols = 36;
    difference() {
        shade_cylinder();
        for (row = [1 : rows])
            for (c = [0 : cols - 1])
                rotate([0, 0, c * 360 / cols + (row % 2) * (180/cols)])
                    translate([d1/2, 0, 14 + row * (shade_height / (rows + 1))])
                        rotate([0, 90, 0])
                            cylinder(h = 2 * shade_wall + 2, d = 8, center = true, $fn = 24);
    }
}
