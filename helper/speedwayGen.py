import copy
import json
import random

import numpy as np


def createArray(num, dimensions):
    array = []
    for i in range(0,3):
        array.append([])

    for j in range(0, dimensions):
            array[0].append(num)
            array[1].append(num)
            array[2].append(num)

    return array


def coutN(m, i, j):
    if m[i][j]==0:
        return 0
    else:
        return m[i-1][j]+m[i+1][j]+m[i][j-1]+m[i][j+1]


def createMap():
    dimensions = 100
    nbRoad = 1
    m = createArray(0, dimensions)
    for i in range(len(m[1])):
        m[1][i]=2
    mf = copy.deepcopy(m)



    return mf





def createTexture(m):
    mf=createArray({},100)
    texH=200
    texW=200

    for i in range(0, 3 ):
        for j in range(0, 100-1):
            if m[i][j] == 0:
                orientation=[0,90,-90,180]
                typeB=["Building","House","Grass","Grass","Grass"]
                mf[i][j] = {
                    "entity": "object",
                    "name": typeB[random.randint(0,len(typeB)-1)],
                    "type": typeB[random.randint(0,len(typeB)-1)],
                    "aabb": [
                        j * texW,
                        i * texH,
                        texW,
                        texH
                    ],
                    "customArgs": {
                        "orientation": orientation[random.randint(0,len(orientation)-1)]
                    }
                }
            if m[i][j] == 1:
                mf[i][j] = {
                    "entity": "object",
                    "name": "House",
                    "type": "House",
                    "aabb": [
                        j * texW,
                        i * texH,
                        texW,
                        texH
                    ],
                    "customArgs": {
                        "orientation": 0
                    }
                }

            if m[i][j]==4:
                mf[i][j]={
                    "entity":"object",
                     "name":"Crossroad",
                     "type":"Crossroad",
                     "aabb":[
                         j * texW,
                         i * texH,
                        texW,
                        texH
                     ],
                     "customArgs":{
                        "orientation":0
                     }
                  }
            if m[i][j]==3:
                orientation = 0
                if m[i][j-1]==0:
                    orientation = 0
                if m[i][j+1]==0:
                    orientation = 180
                if m[i-1][j] == 0:
                    orientation=90
                if  m[i+1][j] == 0:
                    orientation=-90
                mf[i][j]={
                "entity":"object",
                 "name":"HalfRoad",
                 "type":"HalfRoad",
                 "aabb":[
                     j * texW,
                     i * texH,
                    texW,
                    texH
                 ],
                 "customArgs":{
                    "orientation":orientation
                 }
              }
            if m[i][j] == 2:
                if m[i-1][j] !=0 and m[i+1][j]!=0:
                    mf[i][j] = {
                        "entity": "object",
                        "name": "Road",
                        "type": "Road",
                        "aabb": [
                            j * texW,
                            i * texH,
                            texW,
                            texH
                        ],
                        "customArgs": {
                            "orientation": 0
                        }
                    }
                if m[i][j-1] !=0 and m[i][j+1]!=0:
                    mf[i][j] = {
                        "entity": "object",
                        "name": "Road",
                        "type": "Road",
                        "aabb": [
                            j * texW,
                            i * texH,
                            texW,
                            texH
                        ],
                        "customArgs": {
                            "orientation": 90
                        }
                    }
                if m[i][j+1] !=0 and m[i+1][j]!=0:
                    mf[i][j] = {
                        "entity": "object",
                        "name": "Turn",
                        "type": "Turn",
                        "aabb": [
                            j * texW,
                            i * texH,
                            texW,
                            texH
                        ],
                        "customArgs": {
                            "orientation": 180
                        }
                    }
                if m[i][j+1] !=0 and m[i-1][j]!=0:
                    mf[i][j] = {
                        "entity": "object",
                        "name": "Turn",
                        "type": "Turn",
                        "aabb": [
                            j * texW,
                            i * texH,
                            texW,
                            texH
                        ],
                        "customArgs": {
                            "orientation": 90
                        }
                    }
                if m[i][j-1] !=0 and m[i-1][j]!=0:
                    mf[i][j] = {
                        "entity": "object",
                        "name": "Turn",
                        "type": "Turn",
                        "aabb": [
                            j * texW,
                            i * texH,
                            texW,
                            texH
                        ],
                        "customArgs": {
                            "orientation": 0
                        }
                    }
                if m[i][j-1] !=0 and m[i+1][j]!=0:
                    mf[i][j] = {
                        "entity": "object",
                        "name": "Turn",
                        "type": "Turn",
                        "aabb": [
                            j * texW,
                            i * texH,
                            texW,
                            texH
                        ],
                        "customArgs": {
                            "orientation": -90
                        }
                    }
    return mf


m = createMap()
for i in range(0, len(m)):
    print(m[i])
mf = createTexture(m)
for i in range(0, len(m)):
    print(mf[i])
y = np.array(mf)
y = y.flatten()
data={}
data['start']=list(y)
data['configuration'] ={
      "autorun":0,
      "gui":1,
      "printFustrum":1,
      "printVel":0,
      "printInfoMouse":0,
      "simulationDuration":600
   }
data["simulation"]=[]
print(data)
f = open("../scenario/test.json", "w")
json.dump(data, f)