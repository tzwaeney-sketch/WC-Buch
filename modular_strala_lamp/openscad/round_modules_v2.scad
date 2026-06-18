include <module_frame.scad>

// ============================================================
// round_modules_v2.scad -- body modules 03-08
// Each provides an outer decorative shell to mod_frame.
// ============================================================

_min_r = bay_socket_or;   // 43mm

// 03 -- Sphere / Kugel
module body_sphere(h=80, od=mod_typical_d) {
    r = od/2;
    mod_frame(h=h, outer_r=r) {
        hull() {
            translate([0,0,h/2]) scale([1,1, h/od]) sphere(r=r, $fn=96);
            cylinder(h=EPS, r=_min_r, $fn=96);
            translate([0,0,h-EPS]) cylinder(h=EPS, r=_min_r, $fn=96);
        }
    }
}

// 04 -- Flattened sphere / Abgeflacht
module body_flat(h=70, od=mod_typical_d) {
    r = od/2;
    mod_frame(h=h, outer_r=r) {
        hull() {
            translate([0,0,h/2]) scale([1, 0.78, h*0.85/od]) sphere(r=r, $fn=96);
            cylinder(h=EPS, r=_min_r, $fn=96);
            translate([0,0,h-EPS]) cylinder(h=EPS, r=_min_r, $fn=96);
        }
    }
}

// 05 -- Organic S-curve / Organisch
module body_organic(h=90, od=mod_typical_d) {
    r = od/2;
    mod_frame(h=h, outer_r=r) {
        rotate_extrude($fn=128)
            polygon(points = concat(
                [[_min_r, 0]],
                [for (i=[0:1:20])
                    let(z = i/20*h,
                        rr = _min_r + (r-_min_r) * (0.5 + 0.5*sin(360*z/h - 90)) )
                    [max(_min_r, rr), z] ],
                [[_min_r, h]]
            ));
    }
}

// 06 -- Geometric faceted / Geometrisch
module body_geometric(h=80, od=mod_typical_d) {
    r = od/2;
    mod_frame(h=h, outer_r=r) {
        hull() {
            translate([0,0,h*0.5]) cylinder(h=h*0.5, r1=r, r2=_min_r+4, $fn=6);
            translate([0,0,0]) cylinder(h=h*0.5, r1=_min_r+4, r2=r, $fn=6);
            cylinder(h=EPS, r=_min_r, $fn=96);
            translate([0,0,h-EPS]) cylinder(h=EPS, r=_min_r, $fn=96);
        }
    }
}

// 07 -- Narrow ring accent / Schmal_Ring
module body_narrow_ring(h=55, od=88) {
    r = od/2;
    mod_frame(h=h, outer_r=r) {
        union() {
            cylinder(h=h, r=_min_r+2, $fn=96);
            // accent torus ring at mid-height
            translate([0,0,h/2])
                rotate_extrude($fn=128)
                    translate([r - (r-_min_r)/2, 0])
                        circle(r=(r-_min_r)/2, $fn=32);
        }
    }
}

// 08 -- Narrow ribbed / Schmal_Gerippt
module body_narrow_ribbed(h=60, od=88) {
    r = od/2;
    nrib = 24;
    mod_frame(h=h, outer_r=r) {
        union() {
            cylinder(h=h, r=_min_r+1.5, $fn=96);
            for (i=[0:nrib-1])
                rotate([0,0, i*360/nrib])
                    translate([_min_r+1.5, 0, 0])
                        cylinder(h=h, r=(r-_min_r)*0.55, $fn=16);
        }
    }
}

part = "sphere";
if (part=="sphere")        body_sphere();
else if (part=="flat")     body_flat();
else if (part=="organic")  body_organic();
else if (part=="geometric")body_geometric();
else if (part=="ring")     body_narrow_ring();
else if (part=="ribbed")   body_narrow_ribbed();
