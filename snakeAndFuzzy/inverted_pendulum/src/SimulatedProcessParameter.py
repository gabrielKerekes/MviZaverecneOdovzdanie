# -*- coding: utf-8 -*-

try:
    import Tkinter
except ImportError:
    import tkinter
    Tkinter = tkinter
import math

#: Global variable which stores a reference to an existing top-level window
_SingleInstance = None

def Open(process):
    """Open as top-level window."""
    global _SingleInstance
    if _SingleInstance is None:
        _SingleInstance = Tkinter.Toplevel()
        _SingleInstance.title("Simulated Process Parameters")
        _SingleInstance.bind("<Destroy>", _set_None)
        _Window(_SingleInstance,process)
    else:
        _SingleInstance.deiconify()

def Close():
    """Close top-level window."""
    global _SingleInstance
    if _SingleInstance is not None:
        _SingleInstance.destroy()

def _set_None(e=None):
    """If used as top-level window, this is called at "destroy"
       and sets our global variable to None."""
    global _SingleInstance
    _SingleInstance = None


def AddAsSubwidget(root,process):
    """Add the view as subwidget into root."""
    _Window(root,process)

class _Window(object):
    """Gives access to process parameters."""

    def __init__(self,root,process):
        self.process = process
        self.root = root

        row = 0
        self.log_length = Tkinter.DoubleVar(0)
        self.text_length = Tkinter.StringVar()
        Tkinter.Label(self.root,text="length of pendulum").grid(row=row)
        Tkinter.Scale(self.root,showvalue=0,orient=Tkinter.HORIZONTAL,from_=-1,to=1,resolution=0.1,variable=self.log_length).grid(row=row,column=1)
        Tkinter.Label(self.root,text="xxx",textvariable=self.text_length).grid(row=row,column=2)
        self.log_length.trace_variable('w',lambda name,index,mode: self.Length_Changed())

        row = 1
        self.log_mass = Tkinter.DoubleVar(0)
        self.text_mass = Tkinter.StringVar()
        Tkinter.Label(self.root,text="mass of pendulum").grid(row=row)
        Tkinter.Scale(self.root,showvalue=0,orient=Tkinter.HORIZONTAL,from_=0,to=2,resolution=0.1,variable=self.log_mass).grid(row=row,column=1)
        Tkinter.Label(self.root,text="xxx",textvariable=self.text_mass).grid(row=row,column=2)
        self.log_mass.trace_variable('w',lambda name,index,mode: self.Mass_Changed())

        row = 2
        self.log_gain = Tkinter.DoubleVar(0)
        self.text_gain = Tkinter.StringVar()
        Tkinter.Label(self.root,text="gain for incoming acceleration value").grid(row=row)
        Tkinter.Scale(self.root,showvalue=0,orient=Tkinter.HORIZONTAL,from_=-1,to=1,resolution=0.1,variable=self.log_gain).grid(row=row,column=1)
        Tkinter.Label(self.root,text="xxx",textvariable=self.text_gain).grid(row=row,column=2)
        self.log_gain.trace_variable('w',lambda name,index,mode: self.Gain_Changed())

        row = 3
        self.log_disturbance = Tkinter.DoubleVar(0)
        self.text_disturbance = Tkinter.StringVar()
        Tkinter.Label(self.root,text="disturbance").grid(row=row)
        Tkinter.Scale(self.root,showvalue=0,orient=Tkinter.HORIZONTAL,from_=-3,to=1,resolution=0.1,variable=self.log_disturbance).grid(row=row,column=1)
        Tkinter.Label(self.root,text="xxx",textvariable=self.text_disturbance).grid(row=row,column=2)
        self.log_disturbance.trace_variable('w',lambda name,index,mode: self.Disturbance_Changed())


        self.log_length.set(math.log10(process.l)) # length of pendulum [m]
        self.log_mass.set(math.log10(process.m)) # mass of pendulum [kg]

        #self.M_P = 0.1 # friction XXXX [kgm²/s²=Nm]
        #self.a_W = 0.1 # friction of car expressed as acceleration [m/s²]

        self.log_gain.set(math.log10(process.W)) # gain for incoming acceleration value
        self.log_disturbance.set(math.log10(process.Z)) # disturbance

        row = 4
        Tkinter.Button(self.root,text="down",command=self.Down_Pressed).grid(row=row)


    def Length_Changed(self):
        v = math.pow(10.0,self.log_length.get())
        #print v
        self.process.l = v
        self.text_length.set("%4.2f m" % v)

    def Mass_Changed(self):
        v = math.pow(10.0,self.log_mass.get())
        #print v
        self.process.m = v
        self.text_mass.set("%4.2f kg" % v)

    def Gain_Changed(self):
        v = math.pow(10.0,self.log_gain.get())
        #print v
        self.process.W = v
        self.text_gain.set("%4.2f" % v)

    def Disturbance_Changed(self):
        v = math.pow(10.0,self.log_disturbance.get())
        #print v
        self.process.Z = v
        self.text_disturbance.set("%4.2f" % v)

    def Down_Pressed(self):
        self.process.setStateValues({
            "X"      :0.,
            "dX_dT"  :0.,
            "Phi"    :270.,
            "dPhi_dT": 0.
            })
