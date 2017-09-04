#!/usr/bin/env python

acuraccy = 1000                     #1/accuracy cheacks per second
G = 6.67408e-11

class Individual:
    def __init__(self, m, h, s):
        self.mass = m
        self.height = h
        self.speed = s
        self.theta = 90

class Planet:
    def __init__(self, m, r):
        self.radius = r
        self.mass = m

Earth = Planet(5.9723e24, 6.378e6)  #assuming at equator for radius
individuals = []
for num in range(0, 999):
    i = Individual(1000, 0, 0)
    individuals.append(i)



def check_physics(ship, planet):
    r = planet.radius + ship.height
    F = (G * planet.mass)/(r*r)
    print(F)



def update_position(individual):
    individual.height = 5

def control_ship(individual):
    individual.height = 5



for num in range(1, 10000):	        #number of iterations

    for ship in individuals:        #number of ships
        check_physics(ship, Earth)
        update_position(ship)
        control_ship(ship)


