#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main entry point. Starts the application."""

import sys
sys.path.append('../../common/src')
sys.path.append('../../../pyfuzzy')

import simulation.Main

class Main_InvertedPendulum(simulation.Main.Main):
    def getControllers(self):
        """Get list with available controllers."""
        import FuzzyController,FuzzyController2
        import NeuroController
        return \
        [ # available controllers
            ("Fuzzy",FuzzyController.FuzzyController()),
            ("Fuzzy2",FuzzyController2.FuzzyController2()),
            ("Neuro",NeuroController.NeuroController())
        ]

    def getProcesses(self):
        """Get list with available processes."""
        import SimulatedProcess,SimulatedProcessParameter,RealProcess
        return \
        [ # available processes
            ("Simulation",SimulatedProcess.SimulatedProcess(),SimulatedProcessParameter.Open),
            ("Real hardware",RealProcess.RealProcess(),None),
        ]

if __name__ == "__main__":
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    Main_InvertedPendulum().run()
