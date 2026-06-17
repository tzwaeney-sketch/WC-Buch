// =====================================================================
// geometric_modules.scad - Geometric decorative modules
// =====================================================================
include <config.scad>;
include <bayonet_system.scad>;
include <round_modules.scad>;   // reuse _module_frame

// Clean rounded box helper (minkowski of a box with a sphere).
module _rounded_box(s, h, r) {
    minkowski() {
        translate([-(s/2 - r), -(s/2 - r), r])
            cube([s - 2*r, s - 2*r, max(0.01, h - 2*r)]);
        sphere(r = r, $fn = 48);
    }
}

// ---------------------------------------------------------------------
// Rounded cube, h ~ 70mm.
// ---------------------------------------------------------------------
module mod_cube_rounded() {
    h = 70; s = 96; r = 16;
    _module_frame(h) _rounded_box(s, h, r);
}

// ---------------------------------------------------------------------
// Hexagonal prism with rounded edges, h ~ 65mm.
// ---------------------------------------------------------------------
module mod_hexagon() {
    h = 65;
    across = 100;
    _module_frame(h)
        minkowski() {
            linear_extrude(max(0.01, h - 6))
                offset(r = -5)
                    circle(d = across, $fn = 6);
            sphere(r = 3, $fn = 32);
        }
}

// ---------------------------------------------------------------------
// Faceted diamond shape, h ~ 80mm.
// ---------------------------------------------------------------------
module mod_diamond_faceted() {
    h = 80;
    od = 100;
    _module_frame(h)
        union() {
            // lower cone
            cylinder(h = h * 0.45, d1 = od * 0.55, d2 = od, $fn = 8);
            // upper cone
            translate([0, 0, h * 0.45])
                cylinder(h = h * 0.55, d1 = od, d2 = od * 0.45, $fn = 8);
        }
}

// ---------------------------------------------------------------------
// Truncated cone (frustum), h ~ 60mm.
// ---------------------------------------------------------------------
module mod_frustum() {
    h = 60;
    _module_frame(h)
        cylinder(h = h, d1 = 110, d2 = 82, $fn = 96);
}

// ---------------------------------------------------------------------
// Rounded triangular prism, h ~ 65mm.
// ---------------------------------------------------------------------
module mod_triangle_rounded() {
    h = 65;
    across = 110;
    _module_frame(h)
        minkowski() {
            linear_extrude(max(0.01, h - 6))
                offset(r = -6) circle(d = across, $fn = 3);
            sphere(r = 4, $fn = 32);
        }
}

// ---------------------------------------------------------------------
// Stepped cylindrical form, h ~ 75mm.
// ---------------------------------------------------------------------
module mod_stepped_geometric() {
    h = 75;
    steps = 5;
    _module_frame(h)
        for (i = [0 : steps - 1]) {
            d = 110 - i * 8;
            translate([0, 0, i * (h / steps)])
                cylinder(h = h / steps + 0.1, d = d, $fn = 96);
        }
}
