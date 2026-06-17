include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// 13. Teardrop
module mod_teardrop(h=75, outer_d=105) {
    _check(outer_d);
    r=outer_d/2;
    _module_shell(h)
        rotate_extrude($fn=96)
            polygon([[0,0],[r*0.45,0],[r,h*0.35],[r*0.85,h*0.7],[r*0.3,h],[0,h]]);
}

// 14. Vase (S-curve)
module mod_vase(h=85, outer_d=105) {
    _check(outer_d);
    r=outer_d/2;
    base_r = bayonet_interface_outer_radius + 2*structural_wall;
    _module_shell(h)
        rotate_extrude($fn=96)
            polygon([for(i=[0:1:20])
                let(t=i/20, rad = base_r + (r-base_r)*(0.5 + 0.5*sin(360*t - 90)))
                [rad, t*h]
            ]);
}

// 15. Pumpkin (sinusoidal ribs via radial bumps)
module mod_pumpkin(h=65, outer_d=110) {
    _check(outer_d);
    r=outer_d/2;
    _module_shell(h)
        for(a=[0:30:330])
            rotate([0,0,a])
                translate([0,0,h/2])
                    resize([outer_d*0.55, outer_d, h]) sphere(r=r,$fn=48);
}

// 16. Wave (undulating profile)
module mod_wave(h=60, outer_d=105) {
    _check(outer_d);
    r=outer_d/2;
    base_r = bayonet_interface_outer_radius + 2*structural_wall;
    _module_shell(h)
        rotate_extrude($fn=96)
            polygon([for(i=[0:1:24])
                let(t=i/24, rad = base_r + (r-base_r)*(0.6 + 0.4*sin(720*t)))
                [rad, t*h]
            ]);
}

// 17. Organic diamond (hull of offset spheres)
module mod_organic_diamond(h=80, outer_d=100) {
    _check(outer_d);
    r=outer_d/2 - 6;
    _module_shell(h)
        hull() {
            translate([0,0,2]) sphere(r=10,$fn=24);
            translate([0,0,h-2]) sphere(r=8,$fn=24);
            translate([r*0.6, 0, h*0.4]) sphere(r=8,$fn=24);
            translate([-r*0.5, r*0.4, h*0.6]) sphere(r=8,$fn=24);
            translate([0, -r*0.6, h*0.5]) sphere(r=8,$fn=24);
        }
}

// 18. Asymmetric soft (translate+hull)
module mod_asymmetric_soft(h=70, outer_d=105) {
    _check(outer_d);
    r=outer_d/2 - 8;
    _module_shell(h)
        hull() {
            translate([0,0,4]) resize([outer_d,outer_d,20]) sphere(r=r,$fn=48);
            translate([r*0.3,0,h-6]) sphere(r=14,$fn=36);
        }
}

// --- Narrow accent modules ---

// 19. Narrow shadow ring (flat ring)
module mod_narrow_shadow_ring(h=25, outer_d=module_outer_diameter_narrow) {
    _check(outer_d);
    _module_shell(h)
        cylinder(h=h, r=outer_d/2, $fn=96);
}

// 20. Narrow ribbed ring
module mod_narrow_ribbed_ring(h=30, outer_d=module_outer_diameter_narrow) {
    _check(outer_d);
    r=outer_d/2;
    _module_shell(h)
        union() {
            cylinder(h=h, r=r-2, $fn=96);
            for(a=[0:20:340])
                rotate([0,0,a]) translate([r-2,0,0]) cylinder(h=h, r=1.6, $fn=12);
        }
}

if ($preview) mod_teardrop();  // demo: only in GUI preview, skipped on STL export
