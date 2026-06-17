include <config.scad>
include <bayonet_system.scad>

EPS = 0.01;

// 21. Neutral extension (plain tube)
module mod_neutral_extension(h=50, outer_d=module_outer_diameter_narrow) {
    _check(outer_d);
    _module_shell(h)
        cylinder(h=h, r=outer_d/2, $fn=96);
}

// 22. Short spacer
module mod_short_spacer(h=20, outer_d=module_outer_diameter_narrow) {
    _check(outer_d);
    _module_shell(h)
        cylinder(h=h, r=outer_d/2, $fn=96);
}

// 23. Top cap — female bayonet below, 60mm bore stays open,
//     STRÅLA adapter pocket above.
module mod_top_cap(h=40, outer_d=module_outer_diameter_narrow) {
    _check(outer_d);
    bore_r = top_cap_passage_diameter / 2;
    inner_if_r = bayonet_interface_outer_radius + structural_wall;
    pocket_r = strala_socket_outer_diameter/2 + general_clearance;

    difference() {
        union() {
            cylinder(h=h, r=outer_d/2, $fn=96);
        }
        // Through 60mm bore (plug must pass)
        translate([0,0,-EPS]) cylinder(h=h+2*EPS, r=bore_r, $fn=128);
        translate([0,0,-EPS]) cylinder(h=3, r1=bore_r+3, r2=bore_r, $fn=64);
        // STRÅLA socket pocket from the top (concentric, larger than bore)
        translate([0,0,h - strala_socket_total_length*0.4])
            cylinder(h=strala_socket_total_length*0.4 + EPS, r=pocket_r, $fn=64);
    }
    // Female bayonet at bottom only (top cap terminates the stack)
    bayonet_female(h_total=bayonet_working_depth + 2);
}

// 24. Transition (narrow bottom to wide top)
module mod_transition(h=55, bottom_d=module_outer_diameter_narrow, top_d=105) {
    _check(top_d);
    _module_shell(h)
        cylinder(h=h, r1=bottom_d/2, r2=top_d/2, $fn=96);
}

if ($preview) mod_neutral_extension();  // demo: only in GUI preview, skipped on STL export
