include <module_frame.scad>

_tr = bay_socket_or;   // 43mm structural tube radius

module body_sphere(h=80, od=mod_typical_d) {
    mod_frame(h=h, outer_r=od/2) {
        hull() {
            translate([0,0, h/2]) scale([1,1, h/od]) sphere(r=od/2, $fn=96);
            cylinder(h=EPS, r=_tr, $fn=64);
            translate([0,0, h-EPS]) cylinder(h=EPS, r=_tr, $fn=64);
        }
    }
}

module body_flat(h=50, od=mod_typical_d) {
    mod_frame(h=h, outer_r=od/2) {
        hull() {
            translate([0,0, h/2]) scale([1,1, h/od*0.6]) sphere(r=od/2, $fn=96);
            cylinder(h=EPS, r=_tr, $fn=64);
            translate([0,0, h-EPS]) cylinder(h=EPS, r=_tr, $fn=64);
        }
    }
}

module body_organic(h=90, od=mod_typical_d) {
    mod_frame(h=h, outer_r=od/2) {
        hull() {
            cylinder(h=EPS, r=_tr, $fn=64);
            translate([0,0, h*0.35]) cylinder(h=EPS, r=od/2, $fn=64);
            translate([0,0, h*0.65]) cylinder(h=EPS, r=od/2*0.85, $fn=64);
            translate([0,0, h-EPS]) cylinder(h=EPS, r=_tr, $fn=64);
        }
    }
}

module body_geometric(h=80, od=mod_typical_d) {
    mod_frame(h=h, outer_r=od/2) {
        hull() {
            cylinder(h=EPS, r=_tr, $fn=6);
            translate([0,0, h*0.25]) cylinder(h=EPS, r=od/2, $fn=6);
            translate([0,0, h*0.75]) cylinder(h=EPS, r=od/2, $fn=6);
            translate([0,0, h-EPS]) cylinder(h=EPS, r=_tr, $fn=6);
        }
    }
}

module body_narrow_ring(h=55, od=mod_narrow_d) {
    mod_frame(h=h, outer_r=od/2) {
        union() {
            cylinder(h=h, r=od/2, $fn=64);
            translate([0,0, h*0.3]) cylinder(h=h*0.4, r=od/2+4, $fn=64);
        }
    }
}

module body_narrow_ribbed(h=60, od=mod_narrow_d) {
    mod_frame(h=h, outer_r=od/2) {
        union() {
            cylinder(h=h, r=od/2, $fn=64);
            for (i=[0:7])
                rotate([0,0, i*45])
                    translate([od/2-1, 0, 0])
                        cylinder(h=h, r=2.5, $fn=16);
        }
    }
}

part = "sphere";
if      (part == "sphere")          body_sphere();
else if (part == "flat")            body_flat();
else if (part == "organic")         body_organic();
else if (part == "geometric")       body_geometric();
else if (part == "narrow_ring")     body_narrow_ring();
else if (part == "narrow_ribbed")   body_narrow_ribbed();
