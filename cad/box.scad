include <dimensions.scad>
use <MCAD/boxes.scad>
use <ps3eye.scad>


module board_stands(make_hole)
{
    stand_r = make_hole ? arduino_board_mounting_holes_r : arduino_board_mounting_holes_r * 2;
    inc_len = make_hole ? box_dim[2] / 2 : 0;
    
    for(i = [0 : len(arduino_board_mounting_holes_pos) - 1])
    {
        translate([arduino_board_mounting_holes_pos[i][0],
                arduino_board_mounting_holes_pos[i][1],
                -0.1])
        cylinder(h = arduino_board_mounting_holes_h + inc_len,
            r = stand_r,
            $fn = 32);
    }
}


module assembly_stands(make_hole)
{
    stand_r = make_hole ? arduino_board_mounting_holes_r : box_edge_r + 0.2;
    inc_len = make_hole ? 4 * box_wall : 0;
    
    // left bottom
    translate([-box_dim[0] / 2 + box_edge_r + box_wall,
            -box_dim[1] / 2 + box_edge_r + box_wall,
            0])
    cylinder(r = stand_r,
        h = box_dim[2] - 2 * box_wall + 0.1 + inc_len,
        center = true, $fn = 32);

    // left top
    translate([-box_dim[0] / 2 + box_edge_r + box_wall,
            box_dim[1] / 2 - box_edge_r - box_wall,
            0])
    cylinder(r = stand_r,
        h = box_dim[2] - 2 * box_wall + 0.1 + inc_len,
        center = true, $fn = 32);

    // right top
    translate([box_dim[0] / 2 - box_edge_r - box_wall,
            box_dim[1] / 2 - box_edge_r - box_wall,
            0])
    cylinder(r = stand_r,
        h = box_dim[2] - 2 * box_wall + 0.1 + inc_len,
        center = true, $fn = 32);

    // right bottom
    translate([box_dim[0] / 2 - box_edge_r - box_wall,
            -box_dim[1] / 2 + box_edge_r + box_wall,
            0])
    cylinder(r = stand_r,
        h = box_dim[2] - 2 * box_wall + 0.1 + inc_len,
        center = true, $fn = 32);
}


module box()
{
    vent_w = 2;
    n_vent_w = 5;

    difference()
    {
        union()
        {
            difference()
            {
                roundedBox(box_dim, box_edge_r, $fn = 32);
                roundedBox([box_dim[0] - box_wall * 2,
                        box_dim[1] - box_wall * 2,
                        box_dim[2] - box_wall * 2],
                    box_edge_r, $fn = 32);
        
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

            // Board stands
            translate([-box_dim[0] / 2 + box_wall + 5,
                    (box_dim[1] / 2 - box_wall) - arduino_board_dim[1] - 5,
                    -box_dim[2] / 2 + box_wall - 0.1])
            board_stands(false);

            // Stands for box assembly
            assembly_stands(false);

            // Camera mounting step
            translate([
                    -box_dim[0] / 2
                    + box_wall
                    + arduino_board_dim[0]
                    + camera_top_dim[1] / 2
                    + 10,
                    -20 + camera_base_h / 2,
                    0
                ])
            difference()
            {
                roundedBox([camera_base_r * 2, camera_base_h * 2, box_dim[2]],
                    2, true, $fn = 32);
                
                roundedBox([camera_base_r * 2 + 1,
                        camera_base_h * 2 + 1,
                        box_dim[2] / 2],
                    2, true, $fn = 32);
            }
        }    

        translate([-box_dim[0] / 2
                + box_wall
                + arduino_board_dim[0]
                + camera_top_dim[1] / 2
                + 10,
                -20,
                -box_dim[2] / 2 + 20])
        rotate([0, 0, 90])
        rotate([0, 90, 0])
        ps3eye();

        // Board mounting holes through stands and cover
        translate([-box_dim[0] / 2 + box_wall + 5,
                (box_dim[1] / 2 - box_wall) - arduino_board_dim[1] - 5,
                -box_dim[2] / 1.5])
        board_stands(true);
        
        // Stands for box assembly holes
        assembly_stands(true);
    }
    
}


if(ASSEMBLY == undef || ASSEMBLY == 0)
{
    box();
}
