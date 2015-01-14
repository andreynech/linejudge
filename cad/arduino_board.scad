include <dimensions.scad>

module arduino_board()
{
    difference()
    {
        cube(arduino_board_dim);
        for(i = [0 : len(arduino_board_mounting_holes_pos) - 1])
        {
            translate([arduino_board_mounting_holes_pos[i][0],
                    arduino_board_mounting_holes_pos[i][1],
                    -1])
            cylinder(h = arduino_board_dim[2] + 2, r = arduino_board_mounting_holes_r, $fn = 32);
        }
    }
}

arduino_board();
