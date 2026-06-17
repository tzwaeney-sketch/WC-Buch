// =====================================================================
// round_modules.scad - Rounded/spherical decorative modules
// =====================================================================
// Every module: female bayonet at bottom (z=0), male bayonet at top,
// and a clear 55mm bore running through the entire part.
// =====================================================================
include <config.scad>
include <bayonet_system.scad>

// ---------------------------------------------------------------------
// Shared scaffold. Caller supplies a body() child whose total height is
// `body_h` and which is centred on Z axis starting at z=0.
// The scaffold adds bayonets and drills the through bore.
// ---------------------------------------------------------------------
module _module_frame(body_h) {
    fh = bayonet_working_depth + 2;   // female socket depth
    bore = final_plug_passage;
    difference() {
        union() {
            bayonet_female(h = fh);
            translate([0, 0, fh]) children(0);   // the body sits on the socket
            translate([0, 0, fh + body_h]) bayonet_male(h = bayonet_working_depth);
        }
        // Clear through bore for the ENTIRE part
        translate([0, 0, -1])
            cylinder(h = fh + body_h + bayonet_working_depth + 2,
                     d = bore, $fn = fn_large_bore);
        // Chamfer mouths
        _inner_chamfer(bore, 0);
        translate([0,0,fh + body_h + bayonet_working_depth]) mirror([0,0,1])
            _inner_chamfer(bore, 0);
    }
}

// Solid body helper that always reserves the inner bore wall.
module _body_tube_min() {
    cylinder(h = 0.01, d = final_plug_passage + 2 * passage_wall, $fn = fn_large_bore);
}

// ---------------------------------------------------------------------
// Sphere module (h ~ 70mm, OD ~ 100mm). scale_z stretches vertically.
// ---------------------------------------------------------------------
module mod_sphere(scale_z = 1.0) {
    h = 70 * scale_z;
    od = 100;
    _module_frame(h) {
        union() {
            intersection() {
                scale([1, 1, scale_z])
                    translate([0, 0, (h/scale_z)/2]) sphere(d = od, $fn = 96);
                // clip to the module envelope (z = 0 .. h)
                translate([0, 0, h/2]) cube([od + 2, od + 2, h], center = true);
            }
            // Central support tube connects the sphere to the bore wall over
            // the full height so the part is one solid printable body.
            cylinder(h = h, d = final_plug_passage + 2 * structural_wall, $fn = fn_large_bore);
        }
    }
}

// ---------------------------------------------------------------------
// Oblate (flattened) sphere, h ~ 45mm.
// ---------------------------------------------------------------------
module mod_oblate_sphere() {
    h = 45;
    od = 110;
    _module_frame(h)
        union() {
            intersection() {
                scale([1, 1, h / od])
                    translate([0, 0, od/2]) sphere(d = od, $fn = 96);
                cylinder(h = h, d = od + 2, $fn = 96);
            }
            cylinder(h = h, d = final_plug_passage + 2 * structural_wall, $fn = fn_large_bore);
        }
}

// ---------------------------------------------------------------------
// Double sphere (two merged spheres), h ~ 90mm.
// ---------------------------------------------------------------------
module mod_double_sphere() {
    h = 90;
    od = 92;
    _module_frame(h)
        union() {
            intersection() {
                union() {
                    translate([0, 0, od/2 - 4]) sphere(d = od, $fn = 96);
                    translate([0, 0, h - od/2 + 4]) sphere(d = od, $fn = 96);
                    // waist connector
                    translate([0, 0, h/2]) cylinder(h = 14, d = od * 0.7, center = true, $fn = 96);
                }
                // clip to module envelope
                cylinder(h = h, d = od + 2, $fn = 96);
            }
            // central support tube to the bore wall (printable single body)
            cylinder(h = h, d = final_plug_passage + 2 * structural_wall, $fn = fn_large_bore);
        }
}

// ---------------------------------------------------------------------
// Soft cylinder: straight tube with rounded top/bottom edges, h ~ 60mm.
// ---------------------------------------------------------------------
module mod_soft_cylinder() {
    h = 60;
    od = 95;
    r = 12;
    _module_frame(h)
        rotate_extrude($fn = 96)
            translate([0, 0])
                offset(r = r) offset(delta = -r)
                    square([od/2, h]);
}

// ---------------------------------------------------------------------
// Disc: flat disc module, h ~ 35mm.
// ---------------------------------------------------------------------
module mod_disc() {
    h = 35;
    od = 120;
    r = 8;
    _module_frame(h)
        rotate_extrude($fn = 96)
            offset(r = r) offset(delta = -r)
                square([od/2, h]);
}

// ---------------------------------------------------------------------
// Ring / torus-like module, h ~ 40mm.
// ---------------------------------------------------------------------
module mod_ring_module() {
    h = 40;
    od = 110;
    tube_r = h/2;
    ring_center_r = od/2 - tube_r;
    _module_frame(h)
        union() {
            // Torus body
            translate([0, 0, h/2])
                rotate_extrude($fn = 96)
                    translate([ring_center_r, 0]) circle(r = tube_r, $fn = 48);
            // Inner support hub to bore (keeps it printable / connected)
            cylinder(h = h, d = final_plug_passage + 2 * structural_wall + 8, $fn = fn_large_bore);
        }
}
