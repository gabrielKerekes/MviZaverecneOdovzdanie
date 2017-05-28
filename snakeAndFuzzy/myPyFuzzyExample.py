import fuzzy.System
import math

def _createSystem():
    from fuzzy.InputVariable import InputVariable
    from fuzzy.OutputVariable import OutputVariable
    from fuzzy.fuzzify.Plain import Plain
    from fuzzy.defuzzify.COG import COG
    from fuzzy.defuzzify.LM import LM
    from fuzzy.Adjective import Adjective
    from fuzzy.set.Polygon import Polygon

    system = fuzzy.System.System()

    #----------------------------------------------------------------------------------------------------------------
    # input temperature
    #----------------------------------------------------------------------------------------------------------------
    input_temp = InputVariable(fuzzify=Plain())

    system.variables["InputTemp"] = input_temp

    int1_set = Polygon()
    int1_set.add(x =-80, y= 0.0)
    int1_set.add(x = 0.0, y= 1.0)
    int1_set.add(x = 10, y= 0.0)
    int1 = Adjective(int1_set)
    input_temp.adjectives["z"] = int1

    int2_set = Polygon()
    int2_set.add(x = 0, y= 0.0)
    int2_set.add(x = 15, y= 1.0)
    int2_set.add(x = 30, y= 0.0)
    int2 = Adjective(int2_set)
    input_temp.adjectives["s"] = int2

    int3_set = Polygon()
    int3_set.add(x = 15, y= 0.0)
    int3_set.add(x = 30, y= 1.0)
    int3_set.add(x = 80, y= 0.0)
    int3 = Adjective(int3_set)
    input_temp.adjectives["t"] = int3

    #----------------------------------------------------------------------------------------------------------------
    # input wind
    #----------------------------------------------------------------------------------------------------------------
    input_wind = InputVariable(fuzzify=Plain())

    system.variables["InputWind"] = input_wind

    inw1_set = Polygon()
    inw1_set.add(x = 0, y= 0.0)
    inw1_set.add(x = 10.0, y= 1.0)
    inw1_set.add(x = 20, y= 0.0)
    inw1 = Adjective(inw1_set)
    input_wind.adjectives["s"] = inw1

    inw2_set = Polygon()
    inw2_set.add(x = 10, y= 0.0)
    inw2_set.add(x = 30, y= 1.0)
    inw2_set.add(x = 50, y= 0.0)
    inw2 = Adjective(inw2_set)
    input_wind.adjectives["m"] = inw2

    inw3_set = Polygon()
    inw3_set.add(x = 30, y= 0.0)
    inw3_set.add(x = 50, y= 1.0)
    inw3_set.add(x = 150, y= 0.0)
    inw3 = Adjective(inw3_set)
    input_wind.adjectives["v"] = inw3

    #----------------------------------------------------------------------------------------------------------------
    # output => pocitova teplota
    #----------------------------------------------------------------------------------------------------------------
    output_clothes = OutputVariable(defuzzify=COG())

    system.variables["o"] = output_clothes
    output_clothes.failsafe = 0.0 # let it output 0.0 if no COG available

    # out1_set = Polygon()
    # out1_set.add(x = -80, y= 0.0)
    # out1_set.add(x = 0, y= 1.0)
    # out1_set.add(x = 10, y= 0.0)
    # out1 = Adjective(out1_set)
    # output_clothes.adjectives["vz"] = out1

    out2_set = Polygon()
    out2_set.add(x = -80, y= 0.0)
    out2_set.add(x = 0, y= 1.0)
    out2_set.add(x = 10, y= 0.0)
    out2 = Adjective(out2_set)
    output_clothes.adjectives["z"] = out2

    out3_set = Polygon()
    out3_set.add(x = 0, y= 0.0)
    out3_set.add(x = 15, y= 1.0)
    out3_set.add(x = 30, y= 0.0)
    out3 = Adjective(out3_set)
    output_clothes.adjectives["s"] = out3

    out4_set = Polygon()
    out4_set.add(x = 15, y= 0.0)
    out4_set.add(x = 30, y= 1.0)
    out4_set.add(x = 80,  y= 0.0)
    out4 = Adjective(out4_set)
    output_clothes.adjectives["t"] = out4

    # out5_set = Polygon()
    # out5_set.add(x = 30, y= 0.0)
    # out5_set.add(x = 40, y= 1.0)
    # out5_set.add(x = 50, y= 0.0)
    # out5 = Adjective(out5_set)
    # output_clothes.adjectives["vt"] = out5

    #----------------------------------------------------------------------------------------------------------------
    # Definition der Regeln
    #----------------------------------------------------------------------------------------------------------------
    from fuzzy.Rule import Rule
    from fuzzy.norm.Min import Min
    from fuzzy.operator.Input import Input
    from fuzzy.operator.Compound import Compound

    rule1 = Rule(adjective=system.variables["o"].adjectives["z"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["z"]),
                                    Input(system.variables["InputWind"].adjectives["v"])
                                )
                            )
    system.rules["rule1"]=rule1

    rule2 = Rule(adjective=system.variables["o"].adjectives["z"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["z"]),
                                    Input(system.variables["InputWind"].adjectives["m"])
                                )
                            )
    system.rules["rule2"]=rule2

    rule3 = Rule(adjective=system.variables["o"].adjectives["z"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["z"]),
                                    Input(system.variables["InputWind"].adjectives["s"])
                                )
                            )
    system.rules["rule3"]=rule3

    rule4 = Rule(adjective=system.variables["o"].adjectives["z"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["s"]),
                                    Input(system.variables["InputWind"].adjectives["v"])
                                )
                            )
    system.rules["rule4"]=rule4

    rule5 = Rule(adjective=system.variables["o"].adjectives["s"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["s"]),
                                    Input(system.variables["InputWind"].adjectives["m"])
                                )
                            )
    system.rules["rule5"]=rule5

    rule6 = Rule(adjective=system.variables["o"].adjectives["s"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["s"]),
                                    Input(system.variables["InputWind"].adjectives["s"])
                                )
                            )
    system.rules["rule6"]=rule6

    rule7 = Rule(adjective=system.variables["o"].adjectives["s"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["t"]),
                                    Input(system.variables["InputWind"].adjectives["v"])
                                )
                            )
    system.rules["rule7"]=rule7

    rule8 = Rule(adjective=system.variables["o"].adjectives["t"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["t"]),
                                    Input(system.variables["InputWind"].adjectives["m"])
                                )
                            )
    system.rules["rule8"]=rule8

    rule9 = Rule(adjective=system.variables["o"].adjectives["t"],
                                operator=Compound(
                                    Min(),
                                    Input(system.variables["InputTemp"].adjectives["t"]),
                                    Input(system.variables["InputWind"].adjectives["s"])
                                )
                            )
    system.rules["rule9"]=rule9

    return system

input = {
	"InputTemp": 30, "InputWind": 50
}

# input["InputTemp"] = 20
# input["InputWind"] = 20

output = { 
	"o": 0
}

system = _createSystem()
output = system.calculate(input, output)

print output["o"]