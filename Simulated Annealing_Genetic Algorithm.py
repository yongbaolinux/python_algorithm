#!/usr/bin/python
# -*- coding: UTF-8 -*-
## 模拟退火算法和遗传算法

import random
import time
import math
'''##使用模拟退火算法求一元函数极值
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

print simulatedAnnealing(0,100)'''

##航班信息
planes = {}
people = [('zhangsan','BOS'),('lisi','DAL'),('wangwu','CAK'),('wanger','MIA')]

for line in file('./schedule.txt'):
    origin,dest,startTime,arriveTime,price = line.strip().split(',')
    planes.setdefault((origin,dest),[])
    planes[(origin,dest)].append((startTime,arriveTime,price))

'''返回离凌晨的分钟数'''
def getMinutes(t):
    x = time.strptime(t,'%H:%M')
    return x[3] * 60 + x[4]

'''打印行程
    people 用户信息
    wang    所有用户往程行车序号安排
    fan     所有用户返程行车序号安排'''
def printSchedule(people,wang,fan,desc='LGA'):
    ##wang = [1,3,7,6]    ##所有用户往程行车序号安排
    ##fan = [4,2,3,3]     ##所有用户返程行车序号安排
    assert len(wang) == len(fan)
    unit = len(people)
    assert unit == len(wang)

    for i in range(unit):
        name = people[i][0]
        origin = people[i][1]
        wangInfo = planes[(origin,dest)][wang[i]]
        fanInfo = planes[(dest,origin)][fan[i]]
        print '%10s %10s %3s %3s $%3s %3s %3s $%3s' % (name,origin,wangInfo[0],wangInfo[1],wangInfo[2],fanInfo[0],fanInfo[1],fanInfo[2])

'''计算代价 函数 票价=1 往程行程时间=2 返程行程时间=1 往程等待时间=1 返程等待时间=2
    people 用户信息
    wang    所有用户往程行车序号安排
    fan     所有用户返程行车序号安排'''
def calSchedule(people,wang,fan,desc='LGA'):
    cost = 0    ##成本
    unit = len(people)
    assert unit == len(wang) == len(fan)

    price = 0
    wangArriveLatestTime = 0      ##往程最后到达时间初始值
    fanStartEarlyTime = 24*60    ##返程最早启程时间初始值

    wangInfo = [0 for i in range(unit)]
    fanInfo = [0 for i in range(unit)]
    for i in range(unit):
        wangInfo[i] = planes[(people[i][1], dest)][wang[i]]
        fanInfo[i] = planes[(dest, people[i][1])][fan[i]]
        ##价格成本
        price += int(wangInfo[i][2]) + int(fanInfo[i][2])
        ##查找往程最后到达时间和返程最早启程时间
        if wangArriveLatestTime < getMinutes(wangInfo[i][1]):
            wangArriveLatestTime = getMinutes(wangInfo[i][1])
        if fanStartEarlyTime > getMinutes(fanInfo[i][0]):
            fanStartEarlyTime = getMinutes(fanInfo[i][0])

    ##往程等待时间之和
    wangWaitTimeTotal = 0
    fanWaitTimeTotal = 0
    for i in range(unit):
        wangWaitTimeTotal += (wangArriveLatestTime - getMinutes(wangInfo[i][1]))
        fanWaitTimeTotal += (getMinutes(fanInfo[i][0]) - fanStartEarlyTime)
    cost = price * 1 + wangWaitTimeTotal * 1 + fanWaitTimeTotal * 2
    return cost

#printSchedule(people,[1,3,7,6],[4,2,3,3])
#print calSchedule(people,[1,3,7,6],[4,2,3,3])

'''随机搜索 随机产生10000个序列进行计算 找到最优解'''
def randomSearch(people):
    best = 100000
    bestWang = []
    bestFan = []
    for i in range(10000):
        wang = [random.randint(0,9) for i in range(len(people))]
        fan = [random.randint(0,9) for i in range(len(people))]
        cost = calSchedule(people,wang,fan)
        if cost < best:
            best = cost
            bestWang = wang
            bestFan = fan
    return bestWang,bestFan

#wang,fan = randomSearch(people)
#printSchedule(people,wang,fan)

'''爬山搜索'''
def hillClimb(people):
    ##先随机生成一个最优解
    persons = len(people)   #成员数
    wang = [random.randint(0,9) for i in range(persons)]
    fan = [random.randint(0,9) for i in range(persons)]
    cost = calSchedule(people,wang,fan)
    while 1:
        ##获取行程的所有邻近行程
        bestWang = []
        bestFan = []
        bestCost = 100000
        for i in range(persons*2):
            #修改往程 安排
            if i < persons:
                # 在原基础上正负两次波动
                for k in range(-1,2,2):
                    if (wang[i]+k < 0) or (wang[i]+k > 9):
                        continue
                    wang_ = wang[0:i] + [wang[i]+k] + wang[i+1:]
                    cost_ = calSchedule(people,wang_,fan)
                    if(cost_ < bestCost):
                        bestWang = wang_
                        bestFan = fan
                        bestCost = cost_
            #修改返程 安排
            else:
                # 在原基础上正负两次波动 如果小于0 退出本次循环
                for k in range(-1,2,2):
                    if (fan[i-persons]+k < 0) or (fan[i-persons]+k > 9):
                        continue
                    fan_ = fan[0:i-persons] + [fan[i-persons]+k] + fan[i-persons+1:]
                    cost_ = calSchedule(people,wang,fan_)
                    if (cost_ < bestCost):
                        bestWang = wang
                        bestFan = fan_
                        bestCost = cost_
        if(bestCost >= cost):
            return wang,fan
        else:
            wang = bestWang
            fan = bestFan
            cost = bestCost

#wang,fan = hillClimb(people)
#printSchedule(people,wang,fan)


'''模拟退火算法 退火公式 random.random()<pow(math.e , -(新的估值-旧的估值)/T)'''
def simulatedAnnealing(people,T=10000.0,cool=0.95,step=1):
    persons = len(people)
    wang = [random.randint(0,9) for i in range(persons)]
    fan = [random.randint(0,9) for i in range(persons)]
    cost = calSchedule(people,wang,fan)
    while T > 0.1:
        ##pos-变化位置 step-变化方向
        pos = random.randint(0,persons*2-1)
        step_ = random.randint(-step, step)
        if pos >= persons:
            pos -= persons
            if (fan[pos] + step_ < 0) or (fan[pos] + step_ > 9):
                continue
            fan_new = fan[0:pos] + [fan[pos] + step_] + fan[pos+1:]
            cost_ = calSchedule(people,wang,fan_new)
            #接收更优解或者可能接收更差解
            if((cost_ < cost) or (random.random()<pow(math.e , -(cost_ - cost)/T))):
                cost = cost_
                fan = fan_new
        else:
            if (wang[pos] + step_ < 0) or (wang[pos] + step_ > 9):
                continue
            wang_new = wang[0:pos] + [wang[pos] + step_] + wang[pos+1:]
            cost_ = calSchedule(people,wang_new,fan)
            #接收更优解或者可能接收更差解
            if((cost_ < cost) or (random.random()<pow(math.e , -(cost_ - cost)/T))):
                cost = cost_
                wang = wang_new
        T = T * cool

    return wang,fan

wang,fan = simulatedAnnealing(people)
printSchedule(people,wang,fan)

'''遗传算法'''
## 变化 step 变化跨度
def change(wang,fan,step=1):
    wang_ = wang
    fan_ = fan
    len_ = len(wang)
    assert len_ == len(fan)
    i = random.randint(0,len_*2-1)
    if i < len_:
        if(wang[i] + step) <= 9:
            wang_ = wang[0:i] + [wang[i] + step] + wang[i+1:]
        elif(wang[i] - step) >= 0:
            wang_ = wang[0:i] + [wang[i] - step] + wang[i+1:]
    else:
        if (fan[i] + step) <= 9:
            fan_ = fan[0:i] + [fan[i] + step] + fan[i+1:]
        elif (fan[i] - step) >= 0:
            fan_ = fan[0:i] + [fan[i] - step] + fan[i+1:]
    return wang_,fan_

##交叉 pos 交叉点位置
def cross(wang,fan,wang2,fan2,pos=1):
    assert pos>0 and pos<len(wang)-1
    assert len(wang) == len(fan) == len(wang2) == len(fan2)
    return (wang[0:pos] + wang2[pos+1:]),(fan[0:pos]+fan2[pos+1:])

##popSize 初始种群大小
##change
def geneticAlgorithm(popSize=100,changeProp=0.3,top=0.2,generation=100):
