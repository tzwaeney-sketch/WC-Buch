include <config.scad>
include <bayonet_v2.scad>

// ============================================================
// lamp_shades_v2.scad -- three thin-wall shades.
// ============================================================

t        = shade_wall_t;        // 1.6
collar_h = bay_depth;           // 6mm
vent_n   = 12;
vent_r   = shade_vent/2;        // 7.5

br = shade_bot_d/2;             // 120
tr = shade_top_d/2;             // 55

module _frustum_shell() {
    difference() {
        cylinder(h=shade_h, r1=br, r2=tr, $fn=160);
        translate([0,0,-EPS])
            cylinder(h=shade_h+2*EPS, r1=br - t, r2=tr - t, $fn=160);
    }
}

module _vent_ring(z, ring_r) {
    for (i = [0:vent_n-1])
        rotate([0,0, i*360/vent_n + 11])
            translate([0,0,z])
                rotate([0,90,0])
                    cylinder(h=ring_r + 10, r=vent_r, $fn=32);
}

module shade_collar() {
    difference() {
        cylinder(h=collar_h, r=bay_socket_or, $fn=96);
        translate([0,0,-EPS]) cylinder(h=collar_h+2*EPS, r=bay_socket_ir, $fn=96);
        _bay_socket_cuts(collar_h);
        // Center bore for cable/bulb clearance
        translate([0,0,-EPS]) cylinder(h=collar_h+2*EPS, r=bore_r, $fn=96);
    }
}

module shade_classic() {
    difference() {
        union() {
            shade_collar();
            translate([0,0,collar_h])
                _frustum_shell();
        }
        _vent_ring(collar_h + shade_h - 25, tr);
        _vent_ring(collar_h + 35, br);
    }
}

module shade_ribbed() {
    nrib = 36;
    difference() {
        union() {
            shade_collar();
            translate([0,0,collar_h])
                _frustum_shell();
            for (i = [0:nrib-1])
                rotate([0,0, i*360/nrib])
                    hull() {
                        translate([br, 0, collar_h]) cylinder(h=EPS, r=2, $fn=12);
                        translate([tr, 0, collar_h+shade_h]) cylinder(h=EPS, r=1.4, $fn=12);
                    }
        }
        _vent_ring(collar_h + shade_h - 25, tr);
        _vent_ring(collar_h + 35, br);
    }
}

module shade_organic() {
    steps = 60;
    function rmean(z) =
        let(f = z/shade_h)
        (br + (tr - br)*f) + 12*sin(360*f);
    difference() {
        union() {
            shade_collar();
            translate([0,0,collar_h])
                rotate_extrude($fn=160)
                    polygon(points = concat(
                        [ for (i=[0:steps]) let(z=i/steps*shade_h)
                            [ max(rmean(z),     tr - t + 1), z ] ],
                        [ for (i=[steps:-1:0]) let(z=i/steps*shade_h)
                            [ max(rmean(z) - t, tr - t),     z ] ]
                    ));
        }
        _vent_ring(collar_h + shade_h - 25, tr + 12);
        _vent_ring(collar_h + 40, br);
    }
}

part = "classic";
if (part == "classic")      shade_classic();
else if (part == "ribbed")  shade_ribbed();
else if (part == "organic") shade_organic();
