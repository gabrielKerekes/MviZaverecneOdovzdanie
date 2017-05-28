# -*- coding: utf-8 -*-

"""Another fuzyy controller for the inverted pendulum.

@author: Marc Vollmer (modified by Rene Liebscher)
"""


from simulation import Controller

import fuzzy.System
import math

def _createSystem():
    '''
    Definition des Fuzzy-Systems:

        1. Eingangsvariable Phi
        2. Eingangsvariable dPhi_dT
        3. Ausgangsvariable a
        4. Definition der Regeln
    '''
    from fuzzy.InputVariable import InputVariable
    from fuzzy.OutputVariable import OutputVariable
    from fuzzy.fuzzify.Plain import Plain
    from fuzzy.defuzzify.COG import COG
    from fuzzy.Adjective import Adjective
    from fuzzy.set.Polygon import Polygon

    system = fuzzy.System.System()

    #----------------------------------------------------------------------------------------------------------------
    # Definition des Drehwinkels als Eingang
    #----------------------------------------------------------------------------------------------------------------
    input_temp = InputVariable(fuzzify=Plain())

    system.variables["Phi"] = input_temp

    in1_set = Polygon()
    in1_set.add(x =-22.5, y= 0.0)
    in1_set.add(x =  0.0, y= 1.0)
    in1_set.add(x = 22.5, y= 0.0)
    in1 = Adjective(in1_set)
    input_temp.adjectives["eN"] = in1

    in2_set = Polygon()
    in2_set.add(x =  0.0, y= 0.0)
    in2_set.add(x = 22.5, y= 1.0)
    in2_set.add(x = 45.0, y= 0.0)
    in2 = Adjective(in2_set)
    input_temp.adjectives["pk"] = in2

    in3_set = Polygon()
    in3_set.add(x = 22.5, y= 0.0)
    in3_set.add(x = 45.0, y= 1.0)
    in3_set.add(x = 67.5, y= 0.0)
    in3 = Adjective(in3_set)
    input_temp.adjectives["pm"] = in3

    in4_set = Polygon()
    in4_set.add(x = 45.0, y= 0.0)
    in4_set.add(x = 67.5, y= 1.0)
    in4_set.add(x = 90.0, y= 1.0)
    in4_set.add(x =180.0, y= 0.0)
    in4 = Adjective(in4_set)
    input_temp.adjectives["pg"] = in4

    in5_set = Polygon()
    in5_set.add(x = -45.0, y= 0.0)
    in5_set.add(x = -67.5, y= 1.0)
    in5_set.add(x = -90.0, y= 1.0)
    in5_set.add(x =-180.0, y= 0.0)
    in5 = Adjective(in5_set)
    input_temp.adjectives["ng"] = in5

    in6_set = Polygon()
    in6_set.add(x = -22.5, y= 0.0)
    in6_set.add(x = -45.0, y= 1.0)
    in6_set.add(x = -67.5, y= 0.0)
    in6 = Adjective(in6_set)
    input_temp.adjectives["nm"] = in6

    in7_set = Polygon()
    in7_set.add(x =  -0.0, y= 0.0)
    in7_set.add(x = -22.5, y= 1.0)
    in7_set.add(x = -45.0, y= 0.0)
    in7 = Adjective(in7_set)
    input_temp.adjectives["nk"] = in7

    #----------------------------------------------------------------------------------------------------------------
    # Definition der Winkelgeschwindigkeit als Eingang
    #----------------------------------------------------------------------------------------------------------------
    input_tempa = InputVariable(fuzzify=Plain())

    system.variables["dPhi_dT"] = input_tempa

    in1a_set = Polygon()
    in1a_set.add(x =-11.25, y= 0.0)
    in1a_set.add(x =   0.0, y= 1.0)
    in1a_set.add(x = 11.25, y= 0.0)
    in1a = Adjective(in1a_set)
    input_tempa.adjectives["eN"] = in1a

    in2a_set = Polygon()
    in2a_set.add(x =   0.0, y= 0.0)
    in2a_set.add(x = 11.25, y= 1.0)
    in2a_set.add(x = 22.5,  y= 0.0)
    in2a = Adjective(in2a_set)
    input_tempa.adjectives["pk"] = in2a

    in3a_set = Polygon()
    in3a_set.add(x = 11.25, y= 0.0)
    in3a_set.add(x = 22.50, y= 1.0)
    in3a_set.add(x = 33.75, y= 0.0)
    in3a = Adjective(in3a_set)
    input_tempa.adjectives["pm"] = in3a

    in4a_set = Polygon()
    in4a_set.add(x = 22.5,  y= 0.0)
    in4a_set.add(x = 33.75, y= 1.0)
    in4a_set.add(x = 45.0 , y= 1.0)
    in4a_set.add(x = 90.0 , y= 0.0)
    in4a = Adjective(in4a_set)
    input_tempa.adjectives["pg"] = in4a

    in5a_set = Polygon()
    in5a_set.add(x =   -0.0, y= 0.0)
    in5a_set.add(x = -11.25, y= 1.0)
    in5a_set.add(x = -22.5,  y= 0.0)
    in5a = Adjective(in5a_set)
    input_tempa.adjectives["nk"] = in5a

    in6a_set = Polygon()
    in6a_set.add(x = -11.25, y= 0.0)
    in6a_set.add(x = -22.50, y= 1.0)
    in6a_set.add(x = -33.75, y= 0.0)
    in6a = Adjective(in6a_set)
    input_tempa.adjectives["nm"] = in6a

    in7a_set = Polygon()
    in7a_set.add(x = -22.5,  y= 0.0)
    in7a_set.add(x = -33.75, y= 1.0)
    in7a_set.add(x = -45.0 , y= 1.0)
    in7a_set.add(x = -90.0 , y= 0.0)
    in7a = Adjective(in7a_set)
    input_tempa.adjectives["ng"] = in7a

    #----------------------------------------------------------------------------------------------------------------
    # Definition der Horizontalbeschleunigung als Ausgang
    #----------------------------------------------------------------------------------------------------------------
    output_temp = OutputVariable(defuzzify=COG())

    system.variables["a"] = output_temp
    output_temp.failsafe = 0.0 # let it output 0.0 if no COG available

    out1_set = Polygon()
    out1_set.add(x =-0.25, y= 0.0)
    out1_set.add(x =  0.0, y= 1.0)
    out1_set.add(x = 0.25, y= 0.0)
    out1 = Adjective(out1_set)
    output_temp.adjectives["eN"] = out1

    out2_set = Polygon()
    out2_set.add(x = 0.00, y= 0.0)
    out2_set.add(x = 0.25, y= 1.0)
    out2_set.add(x = 0.50, y= 0.0)
    out2 = Adjective(out2_set)
    output_temp.adjectives["pk"] = out2

    out3_set = Polygon()
    out3_set.add(x = 0.25, y= 0.0)
    out3_set.add(x = 0.50, y= 1.0)
    out3_set.add(x = 0.75, y= 0.0)
    out3 = Adjective(out3_set)
    output_temp.adjectives["pm"] = out3

    out4_set = Polygon()
    out4_set.add(x = 0.50, y= 0.0)
    out4_set.add(x = 0.75, y= 1.0)
    out4_set.add(x = 1.0,  y= 1.0)
    out4_set.add(x = 2.0,  y= 0.0)
    out4 = Adjective(out4_set)
    output_temp.adjectives["pg"] = out4

    out5_set = Polygon()
    out5_set.add(x = 0.00, y= 0.0)
    out5_set.add(x =-0.25, y= 1.0)
    out5_set.add(x =-0.50, y= 0.0)
    out5 = Adjective(out5_set)
    output_temp.adjectives["nk"] = out5

    out6_set = Polygon()
    out6_set.add(x =-0.25, y= 0.0)
    out6_set.add(x =-0.50, y= 1.0)
    out6_set.add(x =-0.75, y= 0.0)
    out6 = Adjective(out6_set)
    output_temp.adjectives["nm"] = out6

    out7_set = Polygon()
    out7_set.add(x =-0.50, y= 0.0)
    out7_set.add(x =-0.75, y= 1.0)
    out7_set.add(x =-1.0,  y= 1.0)
    out7_set.add(x =-2.0,  y= 0.0)
    out7 = Adjective(out7_set)
    output_temp.adjectives["ng"] = out7

    #----------------------------------------------------------------------------------------------------------------
    # Definition der Regeln
    #----------------------------------------------------------------------------------------------------------------
    from fuzzy.Rule import Rule
    from fuzzy.norm.Min import Min
    from fuzzy.operator.Input import Input
    from fuzzy.operator.Compound import Compound

    rule1 = Rule(adjective=system.variables["a"].adjectives["pk"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["Phi"].adjectives["nk"]),
                                    Input(system.variables["dPhi_dT"].adjectives["eN"])
                                )
                            )
    system.rules["rule1"]=rule1


    rule2 = Rule(adjective=system.variables["a"].adjectives["nk"],
                            operator=Input(system.variables["Phi"].adjectives["pk"],),
                            )
    system.rules["rule2"]=rule2

    rule3 = Rule(adjective=system.variables["a"].adjectives["pm"],
                            operator=Input(system.variables["Phi"].adjectives["nm"],),
                            )
    system.rules["rule3"]=rule3

    rule4 = Rule(adjective=system.variables["a"].adjectives["nm"],
                            operator=Input(system.variables["Phi"].adjectives["pm"],),
                            )
    system.rules["rule4"]=rule4

    rule5 = Rule(adjective=system.variables["a"].adjectives["pg"],
                            operator=Input(system.variables["Phi"].adjectives["ng"],),
                            )
    system.rules["rule5"]=rule5

    rule6 = Rule(adjective=system.variables["a"].adjectives["ng"],
                            operator=Input(system.variables["Phi"].adjectives["pg"],),
                            )
    system.rules["rule6"]=rule6

    return system


class FuzzyController2(Controller.Controller):
    """
    Fuzzy controller.

    """

    def __init__(self):
        self.system = _createSystem()


    def calculate(self,input={},output={'a':0.0}):
        '''
        Calculates the output value.
        '''
        # this uses 0 as upright position and the range [-180,180]
        input["Phi"] = input["Phi"] - 90.
        if input["Phi"]>180.:
            input["Phi"] = input["Phi"] - 360.
        # this uses radians as angular velocity
        input["dPhi_dT"] = math.radians(input["dPhi_dT"])
        self.system.calculate(input,output)

        return output

    def createDoc(self,directory):
        """Create docs of all variables."""
        from fuzzy.doc.plot.gnuplot import doc
        d = doc.Doc(directory)
        d.createDoc(self.system)
        d.overscan=0
        d.create3DPlot(self.system,"Phi","dPhi_dT","a",{"X":0.,"dX_dT":0.})

    def createDot(self,directory):
        """Create docs of rules."""
        import fuzzy.doc.structure.dot.dot
        import subprocess
        for name,rule in self.system.rules.items():
            cmd = "dot -T png -o '%s/Rule %s.png'" % (directory,name)
            f = subprocess.Popen(cmd, shell=True, bufsize=32768, stdin=subprocess.PIPE).stdin
            fuzzy.doc.structure.dot.dot.print_header(f,"XXX")
            fuzzy.doc.structure.dot.dot.print_dot(rule,f,self.system,"")
            fuzzy.doc.structure.dot.dot.print_footer(f)
        cmd = "dot -T png -o '%s/System.png'" % directory
        f = subprocess.Popen(cmd, shell=True, bufsize=32768, stdin=subprocess.PIPE).stdin
        fuzzy.doc.structure.dot.dot.printDot(self.system,f)
