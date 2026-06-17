include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// 1. Sphere
module mod_sphere(h=75, outer_d=105) {
    _check(outer_d);
    r = outer_d/2;
    _module_shell(h)
        translate([0,0,h/2])
            resize([outer_d, outer_d, h]) sphere(r=r, $fn=96);
}

// 2. Oblate sphere
module mod_oblate_sphere(h=45, outer_d=115) {
    _check(outer_d);
    _module_shell(h)
        translate([0,0,h/2])
            resize([outer_d, outer_d, h]) sphere(r=outer_d/2, $fn=96);
}

// 3. Double sphere
module mod_double_sphere(h=90, outer_d=105) {
    _check(outer_d);
    r = outer_d/2;
    _module_shell(h)
        union() {
            translate([0,0,h*0.28]) resize([outer_d,outer_d,h*0.55]) sphere(r=r,$fn=72);
            translate([0,0,h*0.72]) resize([outer_d*0.85,outer_d*0.85,h*0.55]) sphere(r=r,$fn=72);
        }
}

// 4. Soft cylinder with bulge
module mod_soft_cylinder(h=65, outer_d=105) {
    _check(outer_d);
    r_end = (bayonet_interface_outer_radius + 2*structural_wall);
    _module_shell(h)
        rotate_extrude($fn=96)
            polygon([[0,0],[r_end,0],[r_end,h*0.15],
                     [outer_d/2, h*0.5],
                     [r_end,h*0.85],[r_end,h],[0,h]]);
}

// 5. Disc
module mod_disc(h=35, outer_d=120) {
    _check(outer_d);
    r=outer_d/2;
    _module_shell(h)
        rotate_extrude($fn=128)
            polygon([[0,0],[r-h/2,0],[r,h/2],[r-h/2,h],[0,h]]);
}

// 6. Ring module (torus-like, flat top/bottom)
module mod_ring_module(h=40, outer_d=110) {
    _check(outer_d);
    r=outer_d/2;
    _module_shell(h)
        rotate_extrude($fn=128)
            translate([r - h/2, h/2])
                offset(r=h/2-1) offset(delta=-(h/2-1))
                    square([h/2, h], center=false);
}

if ($preview) mod_sphere();  // demo: only in GUI preview, skipped on STL export
