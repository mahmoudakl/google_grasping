#!/usr/bin/python

#with this function you can test the robot controlability, by using sgs function calls in the console
#basic commands are: 
#sgs.start() - to move the robot into starting position
#sgs.move_tip(y=0.1) - to move the tool tip 10 cm into y direction (or any other direction/orientation - x,y,z,yaw,pitch,roll)

#from bayes_opt import BayesianOptimization
from smart_grasping_sandbox.smart_grasper import SmartGrasper
from tf.transformations import quaternion_from_euler
from math import pi
import time
import rospy
from math import sqrt, pow
import random
from sys import argv
from numpy import var, mean
import numpy as np
#from keras.models import Sequential, Model
#from keras.layers import Dense, Activation, Flatten, Input, Concatenate
#from keras.optimizers import Adam
#from keras.optimizers import sgd
#import keras
import pickle

import pdb

sgs = SmartGrasper()
pdb.set_trace()


