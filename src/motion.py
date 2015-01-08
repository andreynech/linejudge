#! /usr/bin/env python

import random
import math

dt = 1.0 / 30 / 10 # ten times the camera FPS
m_ball = 0.0577
g = 9.8
Fz = - m_ball * g 
k = 0.8

def calc_pos(t, F, m, start_pos, start_velocity):
    return start_pos + start_velocity * t + (F / 2 / m) * t * t


random.seed()

for i in range(0, 5):

    speed = 20 + random.random() * 30
    a = random.random() * math.pi / 6

    # Start conditions in form [(pos0, velocity0), ... ((posN, velocityN))]
    # where N=3 for 3D case
    start = [(0, speed * math.cos(a), 0), 
             (0, random.random() / 100, 0), 
             (2, speed * math.sin(a), Fz)]

    t = 0
    pos = [sp for (sp, _, _) in start]
    z = z_prev = start[2][0]
    while pos[2] > 0:
        pos = [calc_pos(t, F, m_ball, sp, sv) for (sp, sv, F) in start]
        z_prev = z
        z = pos[2]
        print('\t'.join([str(p) for p in pos]))
        t += dt

    t = dt
    start = [(pos[0], start[0][1] * k, start[0][2]), 
             (pos[1], start[1][1] * k, start[1][2]), 
             (pos[2], (z_prev - z) / dt * k, start[2][2])]
    while t < 200 * dt:
        pos = [calc_pos(t, F, m_ball, sp, sv) for (sp, sv, F) in start]
        print('\t'.join([str(p) for p in pos]))
        t += dt

    print('\n')
