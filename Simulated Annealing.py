#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
def F(x):
    return 6*x**7+8*x**6+7*x**3+5*x**2-100*x

def simulatedAnnealing(startX,endX):
    xs = [0 for i in range(10)]
    for i in range(10):
        xs[i] = random.uniform(startX,endX)        ##初始化x的取值

    T = 100
    while T > 0.01:
        for k,v in enumerate(xs):
            value = F(v)
            for i in range(100):
                temp = v + random.uniform(0,100)
                if (temp >= 0) and (temp <= 100):
                    if F(temp) > value:
                        xs[k] = temp
        T = T * 0.98
    max_ = 0
    index = 0
    for v in xs:
        max_ = max(max_,F(v))
        index = v
    return index

print simulatedAnnealing(0,100)
