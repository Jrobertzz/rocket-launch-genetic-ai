#!/usr/bin/env python

#all units are metric base units, ie meters/kilograms
#velocity is m/s
#acceleration is m/s^2

import math
import random

#acuraccy = 1000                                                #1/accuracy cheacks per second
G = 6.67408e-11
target_orbit = 100000                                           #100 km, Kármán line or the edge of space, generally recognized as where the atmosphere ends for Earth

class Individual:
    def __init__(self, m, h, vx, vy, x, y):
        self.flight_time = 0
        self.mass = m
        self.height = h
        self.velocity_x = vx
        self.velocity_y = vy
        self.pos_x = 0.0                                        #assuming launch pad is always at top center relative to observer
        self.pos_y = Earth.radius
        self.thrust_mult = 1
        self.theta = math.pi/2                                  #absolute angle on cartesian coordinates
        self.target_achieved = False
        self.crash = False
        self.start_turn = random.uniform(0, 100)                #seconds atm, 0 - 3000, or 0 to 30 mins after launch 30 mins = 1800; 100 for testing
        self.turn_sensitivity = random.uniform(0, math.pi/2)    #rate at which ship turns, θ = turn_sensitivity * seconds; assumes ~1 degree of change per second possible

class Planet:
    def __init__(self, m, r):
        self.radius = r
        self.mass = m
        self.std_grav_par = G * m                               #standard gravity parameter

Earth = Planet(5.9723e24, 6.378e6)                              #assuming at equator for radius
individuals = []
for num in range(0, 1):
    i = Individual(1000, 0, 0, 0, 0, 0)
    individuals.append(i)
    
def update_position(ship):
    ship.pos_x = ship.pos_x + ship.velocity_x
    ship.pos_y = ship.pos_y + ship.velocity_y
    ship.height = (math.sqrt((ship.pos_x * ship.pos_x) + (ship.pos_y * ship.pos_y)) - Earth.radius) #temporary solution, only works for one planet

def check_gravity(ship, planet):
    r = planet.radius + ship.height
    F = (G * planet.mass)/(r*r)
    return F


def calc_semi_major_axis(ship, planet):
    r = planet.radius + ship.height
    v = math.sqrt((ship.velocity_x * ship.velocity_x) + (ship.velocity_y * ship.velocity_y))
    E = ((v*v)/2) - (planet.std_grav_par/r)
    a = -(planet.std_grav_par/(2 * E))
    return a


def calc_eccentricity_vector(ship, planet):
    r = planet.radius + ship.height
    v = math.sqrt((ship.velocity_x * ship.velocity_x) + (ship.velocity_y * ship.velocity_y))
    e = ((v*v*r)/planet.std_grav_par) - (ship.pos_x + ship.pos_y)/abs(ship.pos_x + ship.pos_y)
    return e

def calc_periapsis(a, e):
    return a * (1 - abs(e))


def calc_apoapsis(a, e):
    return a * (1 + abs(e))

def climb(ship):
    if (ship.flight_time >= ship.start_turn) & (ship.theta >= 0):
        ship.theta = (math.pi/2) - (ship.turn_sensitivity * ((ship.flight_time - ship.start_turn) * (math.pi/180)))

def circularize(ship):
    ship.theta = 1.9 * math.pi                                  #exceedingly rough estimates for testing
    if ((target_orbit - ship.height) / target_orbit) < .005:
        ship.thrust_mult = 1
    else:
        ship.thrust_mult = 0
    print(ship.thrust_mult)

def control_ship(ship, planet):
    a = calc_semi_major_axis(ship, planet)
    e = calc_eccentricity_vector(ship, planet)
    periapsis = calc_periapsis(a, e)
    apoapsis = calc_apoapsis(a, e)
    print("apoapsis: " + str(apoapsis))
    print("periapsis: " + str(periapsis))

    if ship.height < 0:
        ship.crash = True

    if apoapsis < target_orbit + planet.radius:
        climb(ship)
    if (apoapsis >= target_orbit + planet.radius) & (periapsis < target_orbit + planet.radius):
        circularize(ship)
    if (apoapsis >= target_orbit + planet.radius) & (periapsis >= target_orbit + planet.radius):
        return True
    return False

def accel_ship(ship, gravity):
    if ship.pos_x == 0:
        if ship.pos_y > 0:
            grav_angle = math.pi/2
        else:
            grav_angle = math.pi * 1.5
    else:
        grav_angle = 1/(math.atan(ship.pos_y/ship.pos_x))
    ship.velocity_x += (ship.thrust_mult * 15) * math.cos(ship.theta)       #delta v/delta t, TODO: replace with proper forces, including fuel consumption
    ship.velocity_y += (ship.thrust_mult * 15) * math.sin(ship.theta)
    ship.velocity_x -= gravity * math.cos(grav_angle)
    ship.velocity_y -= gravity * math.sin(grav_angle)

for num in range(1, 10000):	                                                #number of iterations

    for ship in individuals:                                                #number of ships, TODO: generalize for more planets than Earth
        if (not ship.target_achieved) & (not ship.crash):
            ship.flight_time += 1
            update_position(ship)
            gravity = check_gravity(ship, Earth)
            ship.target_achieved = control_ship(ship, Earth)
            accel_ship(ship, gravity)
            print("x pos: " + str(ship.pos_x))
            print("y pos: " + str(ship.pos_y))
            print("x vel: " + str(ship.velocity_x))
            print("y vel: " + str(ship.velocity_y))
            print("theta: " + str(ship.theta))
            print("height: " + str(ship.height))
        else:
            break

