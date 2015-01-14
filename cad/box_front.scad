include <dimensions.scad>
use <box.scad>


module box_front()
{
    translate([0, 0, box_dim[2] / 2])
    difference()
    {
        box();

        translate([-box_dim[0] / 2 - 1, -box_dim[1] / 2 - 1, 0])
        cube([box_dim[0] + 2, box_dim[1] + 2, box_dim[2] + 2]);
    }
}

box_front();
