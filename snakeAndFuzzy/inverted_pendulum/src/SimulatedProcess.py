# -*- coding: utf-8 -*-

"""
 Realizes the simulation of the inverted pendulum.

 Calculates the simulation in steps of about 10ms.
 (So we don't need the correct differential equations.)
 
 Beside the movement is also tries to model static and slipping friction.
 Both values are set to the same value and simply modeled as force against 
 the movement direction. If the friction force is larger then the driving 
 force (external or own mass in movement) the movement stops.

 Also contains some modifiable parameters.
"""
from simulation import Process,Pendulum
import math


class SimulatedProcess(Process.Process,Pendulum.Pendulum):
    """Simulation of real process."""


    def __init__(self):
        """Initialize the simulation."""
        Process.Process.__init__(self)
        Pendulum.Pendulum.__init__(self)

        self.X = 0.0  #: position [m]
        self.dX_dT = 0.0 #: velocity [m/s]
        self.Phi = math.radians(45.0) #: angle [rad]
        self.dPhi_dT = 0.0 #: angle velocity [rad/s]

        self.a = 0.0 #: acceleration [m/s²]

        self.l = 1.0 #: length of pendulum [m]
        self.m = 10.0 #: mass of pendulum [kg]
        self.M_P = 0.1 #: friction of bearing of pendulum expressed as torque [kgm²/s²=Nm]
        self.a_W = 0.1 #: friction of car expressed as acceleration [m/s²]

        self.W = 2.0 #: gain for incoming acceleration value
        self.Z = 0.01 #: disturbance

    def setStateValues(self,dict):
        self.X       = dict["X"]
        self.dX_dT   = dict["dX_dT"]
        self.Phi     = math.radians(dict["Phi"])
        self.dPhi_dT = math.radians(dict["dPhi_dT"])

    def getStateValues(self,dict=None):
        dict = dict if dict is not None else {}
        dict["X"]       = self.X
        dict["dX_dT"]   = self.dX_dT
        dict["Phi"]     = math.degrees(self.Phi)
        dict["dPhi_dT"] = math.degrees(self.dPhi_dT)
        return dict

    def setControlValues(self,dict):
        try:
            self.a = dict["a"]
        except KeyError:
            pass # don't change value
        return dict

    def getDefaultControlValues(self):
        return {
                "a":0.0,
        }

