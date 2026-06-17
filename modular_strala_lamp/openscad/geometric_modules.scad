include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// 7. Rounded cube (hull of 8 corner spheres)
module mod_cube_rounded(h=70, outer_d=100) {
    _check(outer_d);
    s = outer_d/2 - 6;
    cr = 6;
    _module_shell(h)
        hull() for(x=[-s,s], y=[-s,s], z=[cr, h-cr])
            translate([x,y,z]) sphere(r=cr, $fn=32);
}

// 8. Hexagonal prism, chamfered
module mod_hexagon(h=65, outer_d=100) {
    _check(outer_d);
    r=outer_d/2;
    _module_shell(h)
        minkowski() {
            cylinder(h=h-4, r=r-2, $fn=6);
            translate([0,0,2]) cylinder(h=0.01, r=2, $fn=24);
        }
}

// 9. Faceted diamond (hull of spheres in diamond arrangement)
module mod_diamond_faceted(h=80, outer_d=100) {
    _check(outer_d);
    r=outer_d/2 - 4;
    _module_shell(h)
        hull() {
            translate([0,0,0]) sphere(r=8,$fn=24);
            translate([0,0,h]) sphere(r=8,$fn=24);
            for(a=[0:60:300])
                rotate([0,0,a]) translate([r,0,h/2]) sphere(r=6,$fn=24);
        }
}

// 10. Frustum (truncated cone, narrow top)
module mod_frustum(h=60, outer_d=100) {
    _check(outer_d);
    _module_shell(h)
        cylinder(h=h, r1=outer_d/2, r2=outer_d/2 - 22, $fn=96);
}

// 11. Rounded triangle (hull of 3 cylinders)
module mod_triangle_rounded(h=65, outer_d=100) {
    _check(outer_d);
    r=outer_d/2 - 12;
    _module_shell(h)
        hull() for(a=[90,210,330])
            rotate([0,0,a]) translate([r,0,0]) cylinder(h=h, r=12, $fn=48);
}

// 12. Stepped geometric (3 stacked cylinders, decreasing diameter)
module mod_stepped_geometric(h=75, outer_d=100) {
    _check(outer_d);
    seg=h/3;
    _module_shell(h)
        union() {
            cylinder(h=seg+EPS, r=outer_d/2, $fn=96);
            translate([0,0,seg]) cylinder(h=seg+EPS, r=outer_d/2 - 12, $fn=96);
            translate([0,0,2*seg]) cylinder(h=seg, r=outer_d/2 - 24, $fn=96);
        }
}

if ($preview) mod_cube_rounded();  // demo: only in GUI preview, skipped on STL export
