#!/usr/bin/python
# -*- coding: UTF-8 -*-
## 神经网络和深度学习识别手写字体

import math
import numpy
import random

class neuralNetworks():
    def __init__(self,layers):
        self.num_layers = len(layers)
        self.layers = layers
        self.biases = [numpy.random.randn(y,1) for y in layers[1:]]
        self.weight = [numpy.random.randn(y,x) for x,y in zip(layers[:-1],layers[1:])]
    def printNetworks(self):
        print self.biases
        print self.weight
    def sigmoid(z):
        return 1.0/(1.0+numpy.exp(-z))

    def feedforward(self):
        

works = neuralNetworks([3,5,2])
#print works.printNetworks()
