tolerance = 0.2;

arduino_board_dim = [116 + 6.3, 65.7 + 6.3, 10];
arduino_board_mounting_holes_h = 3;
arduino_board_mounting_holes_r = 3 / 2 + tolerance;
arduino_board_mounting_holes_pos = [
    [0 + 6.3, 0 + 6.3],
    [0 + 6.3, 52.8 + 6.3],
    [48 + 6.3, 48.8 + 6.3],
    [48 + 6.3, 20 + 6.3],
    [100.1 + 6.3, 53.9 + 6.3],
    [100.3 + 6.3, 5.6 + 6.3]
];

camera_base_r = 52 / 2 + tolerance;
camera_base_h = 6.1 + tolerance;
camera_base_cut = 52 - 41.3;
camera_foot_r = 18 / 2 + tolerance;
camera_foot_h = 3;
camera_sphere_r = 38 / 2;
camera_objective_r = [22 / 2 + tolerance, 21 / 2 + tolerance];
camera_objective_l = 17;
camera_top_dim = [14, 84, 35];
camera_mic_grid_dim = [11, 80.7, 18.7];

box_wall = 2;
box_edge_r = 3;
box_dim = [arduino_board_dim[1] + camera_top_dim[1] + 20, arduino_board_dim[0] + 50, 50];

// LED
led_d = 5 + tolerance / 2; //LED Diameter
led_h = 8.6; //LED Height
led_fh = 1; //LED FLange Thickness
led_fd = 6 + tolerance / 2; //LED Flange Diameter
wire_d = 0.6 + tolerance / 2; //Wire Diameter
wire_h = 27; //Wire Height
wire_da = 2.54; // THe distance between the Wires
