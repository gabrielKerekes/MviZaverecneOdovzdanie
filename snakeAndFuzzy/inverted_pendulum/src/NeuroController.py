# -*- coding: utf-8 -*-

"""Example controller which uses a prelearned neural network 
for controlling the inverted pendulum."""

import math

try:
    import numpy

    # use numpy if available

    def prepareWeightMatrices(weights):
        # build array and transpose
        return numpy.array(weights, numpy.float64).transpose()

    def makeVector(data):
        # build array
        return numpy.array(data,numpy.float64)

    def feedForwardStep(data,weights):
        # calculation uses sigmoidal function
        return 1.0/(1.0+numpy.exp(-1.0*numpy.dot(data,weights)))

except ImportError:

    try:

        import Numeric

        # use Numeric if available

        def prepareWeightMatrices(weights):
            # build array and transpose
            return Numeric.transpose(Numeric.array(weights, Numeric.Float64))

        def makeVector(data):
            # build array
            return Numeric.array(data,Numeric.Float64)

        def feedForwardStep(data,weights):
            # calculation uses sigmoidal function
            return 1.0/(1.0+Numeric.exp(-1.0*Numeric.matrixmultiply(data,weights)))

    except ImportError:

        # otherwise do it manually

        def transpose(matrix):
            """transpose a matrix"""
            return zip(*matrix)

        def vectormatrixmultiply(a,b):
            """multiply vector with matrix.
            b must be transposed"""
            return [sum([a__*b__ for (a__,b__) in zip(a,b_)]) for b_ in b]

        def matrixmatrixmultiply(a,b):
            """multiply two matrices.
            b must be transposed"""
            return [vectormatrixmultiply(a_,b) for a_ in a]

        def applyfuncvector(f,vector):
            """apply function to all elements of vector"""
            return [f(x) for x in vector]

        def applyfuncmatrix(f,matrix):
            """apply function to all elements of matrix"""
            return [applyfuncvector(f,vector) for vector in matrix]

        #---------------------------

        def prepareWeightMatrices(weights):
            """build array and transpose"""
            return transpose(weights)

        def makeVector(data):
            """build vector from list"""
            return data

        def sigmoid(x):
            """sigmoidal function."""
            return 1.0/(1.0+math.exp(-1.0*x))

        def feedForwardStep(data,weights):
            """Feed forward data from one layer to the next through the weight matrix."""
            # calculation uses sigmoidal function
            return applyfuncvector(sigmoid,vectormatrixmultiply(data,transpose(weights))) 

#: weights from input layer to hidden layer 1
input_hidden1 = prepareWeightMatrices((
# first column is bias
[0,0,0,0,0], # create bias in output vector
[1.3523004, -67.2762222, -2.7101681, -1.2252374, -0.1924101],
[3.5358984, -3.0979257, 11.8105240, -2.0400195, -5.6440673],
[2.2998035, -6.4394584, -0.4456880, 13.2240639, -1.9416124],
[-5.3507094, -25.7565060, -0.8581331, -2.4438772, 0.3309670],
[-11.8540325, -27.4872322, -0.4254195, 2.7986245, 0.8198755],
[-2.3312118, -0.4025910, -2.0389884, 3.8539076, 3.2488785],
[-14.8030014, -19.3887348, -2.1227808, -2.5157831, -1.3637272],
[-21.9581738, -38.1970100, -0.7618715, 2.2844830, 1.3290895]
))

#: weights from hidden layer 1 to hidden layer 2
hidden1_hidden2 = prepareWeightMatrices((
# first column is bias
[0,0,0,0,0,0,0,0,0], # create bias in output vector
[-0.2244532, 6.8226333, 5.7899127, 1.6202815, 8.7983570, -15.6285400, 3.5351822, -8.2750082, -6.9833350],
[-14.1263733, -9.2765779, 12.6322460, 0.0562423, -7.2784958, -4.2336187, 6.9077992, 3.8148420, -4.8503165],
[-1.7320144, -2.2005868, -0.0205769, 2.0873408, 3.7128136, -3.4949446, 2.3434448, 7.4144168, -9.0030613],
[-13.3777761, 14.2169991, 6.5337262, -1.3075531, -8.6651535, -24.3653679, 2.9219866, -10.9699783, -7.3186345]
))

#: weights from hidden layer 2 to output layer 2
hidden2_output = prepareWeightMatrices((
# first column is bias
[2.6952314, -2.1971807, -1.7768925, -1.1596987, -3.1659257],
))

#: scaling factor for in-/outputs
arctanh_0_8 = 1.098612


from simulation import Controller
class NeuroController(Controller.Controller):
    """Neural net controller. Trained from data gained
    with the fuzzy controller."""

    def calculate(self,input={},output={}):

        try:
            Phi = input["Phi"]
        except KeyError:
            Phi = 90.0 
        try:
            dPhi_dT = input["dPhi_dT"]
        except KeyError:
            dPhi_dT = 0.0
        try:
            X = input["X"]
        except KeyError:
            X = 0.0
        try:
            dX_dT = input["dX_dT"]
        except KeyError:
            dX_dT = 0.0

        input_ = makeVector((1.0, # bias
                        (Phi-180.0) *2.0/(380.0-(-20.0)),
                        math.tanh(dPhi_dT/500.0 * arctanh_0_8),
                        math.tanh(X/50.0 * arctanh_0_8),
                        math.tanh(dX_dT/20.0 * arctanh_0_8)
                       ))
        # calculation uses sigmoidal function
        hidden1 = feedForwardStep(input_,input_hidden1)
        hidden1[0] = 1.0

        hidden2 = feedForwardStep(hidden1,hidden1_hidden2)
        hidden2[0] = 1.0

        output_ = feedForwardStep(hidden2,hidden2_output)

        output["a"] = (output_[0]*60.0)-30.0

        return output
