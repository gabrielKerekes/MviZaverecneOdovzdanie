# -*- coding: utf-8 -*-

"""The About window for the gui."""

try:
    import Tkinter
except ImportError:
    import tkinter
    Tkinter = tkinter

#: Global variable which stores a reference to an existing top-level window
_SingleInstance = None

def Open():
    """Open as top-level window."""
    global _SingleInstance
    if _SingleInstance is None:
        _SingleInstance = Tkinter.Toplevel()
        _SingleInstance.title("About ...")
        _SingleInstance.bind("<Destroy>", _set_None)
        _Window(_SingleInstance)
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


class _Window(object):
    """'About' window of application."""

    def __init__(self,root):
        self.root = root
        w = Tkinter.Label(self.root,text=
"""
This is a demo application for the PyFuzzy package.

It simulates an inverted pendulum which can be controlled 
by a fuzzy controller or a trained neural network trained from the fuzzy controller.

Author: Rene Liebscher <R.Liebscher@gmx.de>
""")
        w.pack()
