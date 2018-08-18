#!/usr/bin/python

from bayes_opt import BayesianOptimization
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
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam
from keras.optimizers import sgd
import keras
import pickle

import pdb

sgs = SmartGrasper()
pdb.set_trace()

MIN_LIFT_STEPS = 1
# Cut off the action
MAX_BALL_DISTANCE = 0.4

REPEAT_GRASP = 1

# SGS client
# Grasp using parameters fed and return stated when asked
class GraspQuality(object):

    def __init__(self, sgs):
        self.sgs = sgs
        self.last_distance = None
        self.current_grasp = {}

    def check_stable(self, joint_names):
        current_min = 500
        positions = []
        velocities = []
        efforts = []
        for k in range(30):
            sgs.move_tip(y=0.03)
            ball_distance = self.__compute_euclidean_distance()
            if k > MIN_LIFT_STEPS and ball_distance < current_min:
                current_min = ball_distance
                break
            if ball_distance > MAX_BALL_DISTANCE:
                break

            time.sleep(0.5)
        robustness = (1/(current_min - 0.18))**2
        return robustness

    def __compute_euclidean_distance(self):
        ball_pose = self.sgs.get_object_pose()
        hand_pose = self.sgs.get_tip_pose()
        dist = sqrt((hand_pose.position.x - ball_pose.position.x)**2 + \
                     (hand_pose.position.y - ball_pose.position.y)**2 + \
                     (hand_pose.position.z - ball_pose.position.z)**2)
        return dist

    def run_experiments(self, grasp_distance,
                        H1_F1J1, H1_F1J2, H1_F1J3,
                        H1_F2J1, H1_F2J2, H1_F2J3,
                        H1_F3J1, H1_F3J2, H1_F3J3):
        robustness = []
        for _ in range(REPEAT_GRASP):
            robustness.append(self.experiment(grasp_distance,
                                              H1_F1J1, H1_F1J2, H1_F1J3,
                                              H1_F2J1, H1_F2J2, H1_F2J3,
                                              H1_F3J1, H1_F3J2, H1_F3J3))

        # trying to maximize the robustness average - while minimizing its variance
        utility = mean(robustness) / max(0.001,sqrt(var(robustness))) # don't divide by 0

        return utility

    def experiment(self, grasp_distance,
                   H1_F1J1, H1_F1J2, H1_F1J3,
                   H1_F2J1, H1_F2J2, H1_F2J3,
                   H1_F3J1, H1_F3J2, H1_F3J3):
        self.sgs.reset_world()
        time.sleep(0.1)
        self.sgs.reset_world()
        time.sleep(0.1)

        self.sgs.open_hand()
        time.sleep(0.1)
        self.sgs.open_hand()
        time.sleep(0.01)

        ball_pose = self.sgs.get_object_pose()
        ball_pose.position.z += 0.5

        #setting an absolute orientation (from the top)
        quaternion = quaternion_from_euler(-pi/2., 0.0, 0.0)
        ball_pose.orientation.x = quaternion[0]
        ball_pose.orientation.y = quaternion[1]
        ball_pose.orientation.z = quaternion[2]
        ball_pose.orientation.w = quaternion[3]

        self.sgs.move_tip_absolute(ball_pose)
        rospy.loginfo("Moving tip to " + str(ball_pose))

        self.sgs.move_tip(y=grasp_distance)

        # close the grasp
        self.sgs.check_fingers_collisions(False)

        self.current_grasp["H1_F1J1"] = H1_F1J1
        self.current_grasp["H1_F1J2"] = H1_F1J2
        self.current_grasp["H1_F1J3"] = H1_F1J3

        self.current_grasp["H1_F2J1"] = H1_F2J1
        self.current_grasp["H1_F2J2"] = H1_F2J2
        self.current_grasp["H1_F2J3"] = H1_F2J3

        self.current_grasp["H1_F3J1"] = H1_F3J1
        self.current_grasp["H1_F3J2"] = H1_F3J2
        self.current_grasp["H1_F3J3"] = H1_F3J3

        self.sgs.send_command(self.current_grasp, duration=0.5)

        # lift slowly and check the quality
        joint_names = self.current_grasp.keys()

        robustness = self.check_stable(joint_names)

        rospy.loginfo("Grasp quality = " + str(robustness))

        sgs.check_fingers_collisions(True)
        # reward
        return robustness
