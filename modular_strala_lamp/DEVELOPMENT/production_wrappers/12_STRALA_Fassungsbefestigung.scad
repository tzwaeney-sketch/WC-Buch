include </home/user/WC-Buch/modular_strala_lamp/openscad/config.scad>
include </home/user/WC-Buch/modular_strala_lamp/openscad/bayonet_system.scad>
include </home/user/WC-Buch/modular_strala_lamp/openscad/utility_modules.scad>
include </home/user/WC-Buch/modular_strala_lamp/openscad/strala_holder.scad>
mod_top_cap();
translate([bayonet_interface_outer_diameter + 10, 0, 0]) strala_split_clamp_left();
translate([bayonet_interface_outer_diameter + 10 + clamp_od + 5, 0, 0]) strala_split_clamp_right();
