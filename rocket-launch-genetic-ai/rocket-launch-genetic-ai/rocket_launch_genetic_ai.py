#!/usr/bin/env python

#all units are metric base units, ie meters/kilograms
#velocity is m/s
#acceleration m/s^2

import math

acuraccy = 1000                             #1/accuracy cheacks per second
G = 6.67408e-11
taget_orbit = 100000                        #100 km, Kármán line or the edge of space, generally recognized as where the atmosphere ends for Earth

class Individual:
    def __init__(self, m, h, vx, vy, x, y):
        self.mass = m
        self.height = h
        self.velocity_x = vx
        self.velocity_y = vy
        self.pos_x = Earth.radius + x
        self.pos_y = 0                      #assuming launch pad is always at top center relative to observer
        self.theta = 90                     #absolute angle on cartesian coordinates

class Planet:
    def __init__(self, m, r):
        self.radius = r
        self.mass = m
        self.std_grav_par = G * m           #standard gravity parameter

Earth = Planet(5.9723e24, 6.378e6)          #assuming at equator for radius
individuals = []
for num in range(0, 999):
    i = Individual(1000, 0, 0, 0, 0, 0)
    individuals.append(i)


    

def update_position(ship):
    ship.pos_x = ship.pos_x + ship.velocity_x
    ship.pos_y = ship.pos_y + ship.velocity_y

def check_gravity(ship, planet):
    r = planet.radius + ship.height
    F = (G * planet.mass)/(r*r)
    print(F)


def calc_semi_major_axis(ship, planet):
    r = planet.radius + ship.height
    v = math.sqrt((ship.velocity_x * ship.velocity_x) + (ship.velocity_y * ship.velocity_y))
    E = ((v*v)/2) - (planet.std_grav_par/r)
    a = -(planet.std_grav_par/(2 * E))
    return a


def calc_eccentricity_vector(ship, planet):
    r = planet.radius + ship.height
    v = math.sqrt((ship.velocity_x * ship.velocity_x) + (ship.velocity_y * ship.velocity_y))
    e = ((v*v*r)/planet.std_grav_par) - ((r*v*v)/planet.std_grav_par) - r/abs(r)
    return e

def calc_periapsis(a, e):
    return a * (1 - abs(e))

def calc_apoapsis(a, e):
    return a * (1 + abs(e))

def control_ship(ship, planet):
    a = calc_semi_major_axis(ship, planet)
    e = calc_eccentricity_vector(ship, planet)
    periapsis = calc_periapsis(a, e)
    apoapsis = calc_apoapsis(a, e)

    #if apoapsis < target_orbit:
        #ai climb

for num in range(1, 10000):	                #number of iterations

    for ship in individuals:        #number of ships, TODO: generalize for more planets than Earth
        update_position(ship)
        check_gravity(ship, Earth)
        control_ship(ship, Earth)


