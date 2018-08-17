#https://thecodacus.com/neural-network-scratch-python-no-libraries/#.Wz42r9JKiUl
import math
import numpy as np
import pickle
import time

class Connection:
    def __init__(self, connectedNeuron, use_existing_weight):
        self.connectedNeuron = connectedNeuron
        self.weight = np.random.normal()
        self.dWeight = 0.0


class Neuron:
    def __init__(self, layer, weight):
        self.dendrons = []
        self.error = 0.0
        self.gradient = 0.0
        self.output = 0.0
        if layer is None:
            pass
        else:
            for neuron in layer:
                con = Connection(neuron, None)
                self.dendrons.append(con)
    
    def addError(self, err):
        self.error = self.error + err

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x * 1.0))

    def dSigmoid(self, x):
        return x * (1.0 - x)

    def setError(self, err):
        self.error = err

    def setOutput(self, output):
        self.output = output

    def getOutput(self):
        return self.output

    def feedForword(self):
        sumOutput = 0
        if len(self.dendrons) == 0:
            return
        for dendron in self.dendrons:
            sumOutput = sumOutput + dendron.connectedNeuron.getOutput() * dendron.weight
        self.output = self.sigmoid(sumOutput)

    def backPropagate(self):
        self.gradient = self.error * self.dSigmoid(self.output)
        for dendron in self.dendrons:
            dendron.dWeight = Neuron.eta * (
            dendron.connectedNeuron.output * self.gradient) + self.alpha * dendron.dWeight
            dendron.weight = dendron.weight + dendron.dWeight
            dendron.connectedNeuron.addError(dendron.weight * self.gradient)
        self.error = 0


class Network:
    def __init__(self, topology):
        self.layers = []
        for numNeuron in topology:
            layer = []
            for i in range(numNeuron):
                if len(self.layers) == 0:
                    layer.append(Neuron(None, None))
                else:
                    layer.append(Neuron(self.layers[-1], None))
            layer.append(Neuron(None, None))
            layer[-1].setOutput(1)
            self.layers.append(layer)

    def setInput(self, inputs):
        for i in range(len(inputs)):
            self.layers[0][i].setOutput(inputs[i])

    def feedForword(self):
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.feedForword()

    def backPropagate(self, target):
        for i in range(len(target)):
            self.layers[-1][i].setError(target[i] - self.layers[-1][i].getOutput())
        for layer in self.layers[::-1]:
            for neuron in layer:
                neuron.backPropagate()

    def getError(self, target):
        err = 0
        for i in range(len(target)):
            e = (target[i] - self.layers[-1][i].getOutput())
            err = err + e ** 2
        err = err / len(target)
        err = math.sqrt(err)
        return err

    def getResults(self):
        output = []
        for neuron in self.layers[-1]:
            output.append(neuron.getOutput())
        output.pop()
        return output

    def getThResults(self, exact):
        output = []
        for neuron in self.layers[-1]:
            o = neuron.getOutput()
            if exact == False:
                if o > 0.5:
                    o = 1
                else:
                    o = 0
            output.append(o)
        output.pop()
        return output


#def alpha_changer(x, og):
#    x -= x*0.03
#    return(x)


def train(topology, inputs, outputs, use_saved, hrs, new_alpha, new_eta):
    global net

    if use_saved:
        file = open('network', 'rb')
        net = pickle.load(file)
    else:
        net = Network(topology)

    if hrs > 0:
        lowest_error = 100000
        max_alpha = 0.01
        no_improvement = 0
        iteration = 0
        increase = False
        error_saved = []

        inital_set = False

        t = time.time()

        Neuron.alpha = new_alpha
        Neuron.eta = new_eta
        
        while True:
            err = 0

            #Neuron.alpha = alpha_changer(Neuron.alpha, new_alpha)
            #print("Alpha: {}".format(Neuron.alpha))
            
            for i in range(len(inputs)):
                net.setInput(inputs[i])
                net.feedForword()
                net.backPropagate(outputs[i])
                err = err + net.getError(outputs[i])
            print("Error: "+str(err))
            error_saved.append(err)
            
            iteration += 1
            
            if err < lowest_error:
                lowest_error = err
                print("New Low Acheived - Weights Saved")
                name = 'network-alpha {0}-eta {1}'.format(str(new_alpha), str(new_eta))
                with open(name, "wb") as fp:
                    pickle.dump(net, fp)
                print("Network saved")
            
            t_new = time.time()
            if t_new - t > 60*60*hrs:
                break
            else:
                print("Iteration {0}".format(iteration))
                print("Hours Trained: {0}\n".format((t_new-t)/60/60))

def guess(i, exact):
    global net
    net.setInput(i)
    net.feedForword()
    return net.getThResults(exact)

