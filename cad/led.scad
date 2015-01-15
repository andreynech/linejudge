include <dimensions.scad>


module led()
{
    translate([0, 0, led_fh])
    cylinder(led_h - led_d / 2 - led_fh, led_d / 2, led_d / 2, $fn = 32);
    
    translate([0, 0, led_h - led_d / 2])
    sphere(led_d / 2, $fn = 32);

    cylinder(led_fh, led_fd / 2, led_fd / 2, $fn = 32);
    
    translate([0, wire_da / 2, -wire_h])
    cylinder(wire_h, wire_d / 2, wire_d / 2, $fn = 32);
    
    translate([0, wire_da / -2, -wire_h])
    cylinder(wire_h, wire_d / 2, wire_d / 2, $fn = 32);
}

if(ASSEMBLY == undef || ASSEMBLY == 0)
{
    led();
}
