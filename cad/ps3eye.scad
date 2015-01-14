include <dimensions.scad>
use <MCAD/boxes.scad>

module cut_cube()
{
    cut_cube_xdim = 30;
    
    translate([-camera_top_dim[2] / 2 - cut_cube_xdim, 0, -camera_top_dim[0] / 2 - 1])
    rotate([0, 0, -15])
    cube([cut_cube_xdim, camera_top_dim[1] * 2, camera_top_dim[0] + 2]);
}


module ps3eye()
{    
    // Cuttet round base
    difference()
    {
        cylinder(r = camera_base_r, h = camera_base_h, $fn = 128);
        
        translate([camera_base_r - camera_base_cut, -camera_base_r, -1])
        cube([camera_base_r, 2 * camera_base_r, camera_base_h + 2]);
    }

    // Foot
    translate([0, 0, camera_base_h])
    cylinder(r = camera_foot_r, h = camera_foot_h + 5, $fn = 128);
    // +5 height to close the gap between sphere and foot

    // Spherical body
    translate([0, 0, camera_base_h + camera_foot_h + camera_sphere_r])
    sphere(r = camera_sphere_r, $fn = 128);

    // Objective
    translate([camera_sphere_r - 5,
            0,
            camera_base_h + camera_foot_h + camera_sphere_r])
    rotate([0, 90, 0])
    cylinder(r1 = camera_objective_r[0],
        r2 = camera_objective_r[1],
        h = camera_objective_l + 5, $fn = 128);

    // Top boxed part
    translate([0, 0, camera_base_h + camera_foot_h + 2 * camera_sphere_r])
    rotate([0, -90, 0])
    {
        difference()
        {
            roundedBox([camera_top_dim[2],
                    camera_top_dim[1],
                    camera_top_dim[0]], 5, true);
            
            cut_cube();
            mirror([0, 1, 0])
            cut_cube();
        }
    }

    // Microphone grid
    translate([5,
            0,
            camera_base_h
            + camera_foot_h
            + 2 * camera_sphere_r
            + camera_top_dim[2] / 2
            - camera_mic_grid_dim[2] / 2 - 1
        ])
    color("DarkGray")
    rotate([0, 90, 0])
    roundedBox([camera_mic_grid_dim[2],
            camera_mic_grid_dim[1],
            camera_mic_grid_dim[0]], 3, $fn = 32);

    // Status LEDs
    translate([camera_top_dim[0] / 2, -15, 30])
    color("Red")
    sphere(r = 1, $fn=16);
    mirror([0, 1, 0])
    {
        translate([camera_top_dim[0] / 2, -15, 30])
        color("Blue")
        sphere(r = 1, $fn=16);
    }
}


ps3eye();
