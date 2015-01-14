include <dimensions.scad>
use <box.scad>


module box_back()
{
    rotate([180, 0, 0])
    difference()
    {
        box();

        translate([-box_dim[0] / 2 - 1, -box_dim[1] / 2 - 1, -box_dim[2] / 2 - 1])
        cube([box_dim[0] + 2, box_dim[1] + 2, box_dim[2] / 2 + 1]);
    }
}


if(ASSEMBLY == undef || ASSEMBLY == 0)
{
    box_back();
}
