#! /usr/bin/env python

import random
import math
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

dt = 1.0 / 30
m_ball = 0.0577
g = 9.8
Fz = - m_ball * g 
k = 0.8

def calc_pos(t, F, m, start_pos, start_velocity):
    return start_pos + start_velocity * t + (F / 2 / m) * t * t


random.seed()

speed = 20 + random.random() * 30
a = random.random() * math.pi / 6

# Start conditions in form [(pos0, velocity0), ... ((posN, velocityN))]
# where N=3 for 3D case
start = [(0, speed * math.cos(a), 0), 
         (0, random.random() / 100, 0), 
         (2, speed * math.sin(a), Fz)]

trajectory = []
t = 0
pos = [sp for (sp, _, _) in start]
z = z_prev = start[2][0]

while pos[2] > 0:
    pos = [calc_pos(t, F, m_ball, sp, sv) for (sp, sv, F) in start]
    z_prev = z
    z = pos[2]
    trajectory.append(pos)
    t += dt

t = dt
start = [(pos[0], start[0][1] * k, start[0][2]), 
         (pos[1], start[1][1] * k, start[1][2]), 
         (pos[2], (z_prev - z) / dt * k, start[2][2])]
while t < 20 * dt:
    pos = [calc_pos(t, F, m_ball, sp, sv) for (sp, sv, F) in start]
    trajectory.append(pos)
    t += dt

idx = 0
for j in range(0, len(trajectory)):
    if trajectory[j][2] < 0:
        idx = j
        break
    
#x = np.array([pos[0] for pos in trajectory[idx - 5 : idx]])
#z = np.array([pos[2] for pos in trajectory[idx - 5 : idx]])
x = np.array([pos[0] for pos in trajectory[0 : idx]])
z = np.array([pos[2] for pos in trajectory[0 : idx]])
f = UnivariateSpline(x, z)

xnew = np.linspace(x.min(), x.max() + 2, 128)
plt.plot(x, z, 'o', xnew, f(xnew), '-')
plt.legend(['Data', 'Univariate spline'], loc='best')
plt.grid(True)
plt.show()
