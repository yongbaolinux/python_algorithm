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
        ##self.biases = [numpy.random.randn(y,1) for y in layers[1:]]
        self.biases = [numpy.array([[-0.13186037],
                                    [-0.35103704],
                                    [-1.28473365],
                                    [-0.33773115],
                                    [ 1.53916219]]),
                       numpy.array([[-1.52530996],
                                    [ 2.35564107]])]
        ##self.weight = [numpy.random.randn(y,x) for x,y in zip(layers[:-1],layers[1:])]
        self.weight = [numpy.array([[-0.49459404, -2.44160808, -1.47850901],
                                [ 1.52973182,  0.62470849, -1.74214583],
                                [ 2.43524424,  0.98527557,  1.79066377],
                                [-0.04521586, -0.89447031, -0.56162334],
                                [ 0.9707984 ,  0.84499252,  1.9669763 ]]),
                       numpy.array([[ 2.81669599, -0.33279294,  0.37467263,  0.33384075,  0.11570302],
                                    [ 2.5417848 , -0.91537258, -1.10099304, -0.99188506, -0.81890493]])]

    ##打印神经网络权重和参数
    def printNetworks(self):
        print self.biases
        print self.weight

    ##S型函数
    def sigmoid(slef,z):
        return 1.0/(1.0+pow(math.e,(-z)))

    ##前馈计算函数
    def feedforward(self,input):
        # input 为输入数据
        for x,y in zip(self.biases,self.weight):
            #print x
            #第一层隐藏层计算后得到的输出input是一个数组 然后作为第二层的输入进行第二次计算
            input =  self.sigmoid(numpy.dot(y,input)+x)
        return input
    ##
    
works = neuralNetworks([3,5,2])

works.feedforward([[1],[2],[3]])

# print zip([ [[1],
#             [2],
#             [3],
#             [4],
#             [5]],
#
#             [[6],
#             [7]],9],[[            [-0.49459404, -2.44160808, -1.47850901],
#                                 [ 1.52973182,  0.62470849, -1.74214583],
#                                 [ 2.43524424,  0.98527557,  1.79066377],
#                                 [-0.04521586, -0.89447031, -0.56162334],
#                                 [ 0.9707984 ,  0.84499252,  1.9669763 ]],
#
#                                 [[ 2.81669599, -0.33279294,  0.37467263,  0.33384075,  0.11570302],
#                                     [ 2.5417848 , -0.91537258, -1.10099304, -0.99188506, -0.81890493]],[10]])

