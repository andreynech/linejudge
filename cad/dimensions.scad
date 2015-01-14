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

camera_base_r = 50 / 2;
camera_base_h = 3;
camera_base_cut = 15;
camera_foot_r = 15 / 2;
camera_foot_h = 3;
camera_sphere_r = 30 / 2;
camera_objective_r = [18 / 2 + tolerance, 16 / 2];
camera_objective_l = 10;
camera_top_dim = [10, 70, 30];
camera_mic_grid_dim = [10, 50, 10];

box_wall = 2;
box_dim = [arduino_board_dim[0] + camera_top_dim[1] + 20, arduino_board_dim[1] + 50, 60];
