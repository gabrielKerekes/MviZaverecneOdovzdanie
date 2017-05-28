# -*- coding: utf-8 -*-

try:
    import Tkinter
except ImportError:
    import tkinter
    Tkinter = tkinter

#: Global variable which stores a reference to an existing top-level window
_SingleInstance = None

def Open(system):
    """Open as top-level window."""
    global _SingleInstance
    if _SingleInstance is None:
        _SingleInstance = Tkinter.Toplevel()
        _SingleInstance.title("Process View")
        _SingleInstance.bind("<Destroy>", _set_None)
        _Window(_SingleInstance,system)
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


def AddAsSubwidget(root,system):
    """Add the process view as subwidget into root."""
    _Window(root,system)


import math

class _Window(object):
    """Shows current process state."""

    _update_time = 50 #: ms 
    _width = 3 #: radius
    _scale_x = 50
    _scale_length = 50
    _canvas_width = 530
    _canvas_height = 400

    def __init__(self,root,system):
        self.system = system
        self.root = root
        self.canvas = Tkinter.Canvas(self.root,width=self._canvas_width,height=self._canvas_height)
        l = self.system.process.l*self._scale_length
        x = 0
        y = 0
        x_end = l*math.cos(math.pi/2.0)
        y_end = l*math.sin(math.pi/2.0)
        h = self._canvas_height
        w = self._canvas_width
        r = self._width
        self.yzeroaxis = self.canvas.create_line((0,h/2,w,h/2),width=1)
        self.xzeroaxis = self.canvas.create_line((w/2,0,w/2,h),width=1,fill="red")
        self.pole = self.canvas.create_line((x,y,x_end,y_end),width=r*2.0,capstyle="round")
        self.origin = self.canvas.create_oval((x-r,y-r,x+r,y+r),fill="white")
        self.canvas.pack()

        self.output = Tkinter.Text(self.root,width=80,height=1)
        self.output.pack()
        self.update()

    def update(self):
        """regularly called update of visualization."""
        # base params of visualization
        h = self._canvas_height
        w = self._canvas_width
        r = self._width

        # get values
        v = self.system.process.getStateValues()
        x = v['X']*self._scale_x+w/2
        phi = math.radians(v['Phi'])
        l = self.system.process.l*self._scale_length

        # graphical output
        # xzeroline
        if x >= w:
            self.canvas.coords(self.xzeroaxis,1,0,1,h)
        elif x < 0:
            self.canvas.coords(self.xzeroaxis,w-1,0,w-1,h)
        else:
            self.canvas.coords(self.xzeroaxis,w/2,0,w/2,h)

        # position of pendulum
        x = x % w
        y = h/2
        x_end = x+l*math.cos(phi)
        y_end = y-l*math.sin(phi)
        self.canvas.coords(self.pole,x,y,x_end,y_end)
        self.canvas.coords(self.origin,x-r,y-r,x+r,y+r)

        # text output
        text = "Phi:%5.1f | dPhi_dT:%6.1f | X:%6.1f | dX_dT:%6.3f\n" % (v['Phi'],v['dPhi_dT'],v['X'],v['dX_dT'])
        self.output.insert("1.0",text)
        self.output.delete("2.0","3.0")

        # recall self after some time
        self.root.after(self._update_time,self.update)
