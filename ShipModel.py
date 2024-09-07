import numpy as np
import random
import math
from controller import pid_controller

class Ship:
    def __init__(self):
        # Dynamic states
        self.position = 0.0
        self.velocity = 0.0
        self.rps = 0  # Revolutions per second for propeller (control input)
        
        # Vessel parameters
        self.mass = 10  # Mass of the ship
        self.CD0 = 0.25  # Drag coefficient
        self.Area = 0.04  # Frontal area for drag calculations
        self.propellerDiameter = 0.04
        self.KT0 = 0.4  # Propeller thrust constant
        self.RO = 1025  # Density of water
        self.max_rps = 5000/60

        # Control parameters
        self.control_active = False  # Toggle for control
        self.setpoint = 0  # Desired position (setpoint)

        # PD Controller parameters
        self.Kp = 0 # Proportional gain
        self.Ki = 0 #Integral gain
        self.Kd = 0  #Derivative gain
        self.previous_error = 0.0  # To store the previous error for the derivative term
        self.integral_error = 0.0 # To store the accumulated error ( integral )
        

    def update_dynamics(self, dt):
        if self.control_active:
            # Kall PID-kontrolleren fra controller.py og send Ship-objektet
            pid_controller(self, dt)

        # Beregn thrust og dynamikken
        thrust = 0.5 * self.RO * self.KT0 * (self.propellerDiameter ** 4) * abs(self.rps) * self.rps
        drag = 0.5 * self.CD0 * self.RO * self.Area * abs(self.velocity) * self.velocity
        acceleration = (thrust - drag) / self.mass

        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        return self.position