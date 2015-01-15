ASSEMBLY = 1;

use <ps3eye.scad>
use <box_front.scad>
use <box_back.scad>
include <dimensions.scad>

box_front();

translate([-box_dim[0] / 2
        + box_wall
        + arduino_board_dim[1]
        + camera_top_dim[1] / 2
        + 10,
        -20,
        20])
rotate([0, 0, 90])
rotate([0, 90, 0])
color("DimGray")
ps3eye();

translate([30, 0, 110])
rotate([0, 45, 0])
rotate([180, 0, 0])
box_back();

translate([0, 0, 100])
%cube([200, 200, 200], center = true);
