include <dimensions.scad>
use <MCAD/boxes.scad>
use <ps3eye.scad>


module board_stands()
{
    for(i = [0 : len(arduino_board_mounting_holes_pos) - 1])
    {
        translate([arduino_board_mounting_holes_pos[i][0],
                arduino_board_mounting_holes_pos[i][1],
                -1])
        difference()
        {
            cylinder(h = arduino_board_dim[2] + 2, r = arduino_board_mounting_holes_r * 3, $fn = 32);
            cylinder(h = arduino_board_dim[2] + 2, r = arduino_board_mounting_holes_r, $fn = 32);
        }
    }
}


module box()
{
    edge_r = 5;
    vent_w = 2;
    n_vent_w = 6;
    
    difference()
    {
        roundedBox(box_dim, edge_r);
        roundedBox([box_dim[0] - box_wall,
                box_dim[1] - box_wall,
                box_dim[2] - box_wall],
            edge_r, $fn = 16);

        // Ventilation top/bottom
        roundedBox([box_dim[0] / 2,
                box_dim[1] * 2,
                box_dim[2] / 8],
            2, $fn = 16);
        // Ventilation back side
        for(x = [-n_vent_w * (vent_w + 2 * vent_w) : vent_w + 2 * vent_w : n_vent_w * (vent_w + 2 * vent_w)])
        {
            translate([x, 0, box_dim[2] / 2 - box_wall / 2])
            roundedBox([vent_w, box_dim[1] / 2, 2 * box_wall], 1, 0, $fn = 16);
        }
    }

    translate([-box_dim[0] / 2 + box_wall,
            (box_dim[1] / 2 - box_wall) - arduino_board_dim[1],
            -box_dim[2] / 2 + box_wall - 0.1])
    board_stands();
        
    translate([-box_dim[0] / 2 + box_wall + arduino_board_dim[0] + camera_top_dim[1] / 2 + 10,
            0,
            -box_dim[2] / 2 + 20])
    rotate([0, 0, 90])
    rotate([0, 90, 0])
    #ps3eye();
}


box();
