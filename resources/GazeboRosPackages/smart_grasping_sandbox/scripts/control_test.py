#!/usr/bin/python

import os
from smart_grasping_sandbox.smart_grasper import SmartGrasper
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import  SpawnEntity, DeleteModel, GetWorldProperties, GetModelState
import rospy
import pdb

__spawn_model = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnEntity)
__delete_model = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)
__get_world_properties = rospy.ServiceProxy("/gazebo/get_world_properties", GetWorldProperties)
__get_model_state = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)
__path_to_models = os.getenv("HOME") + "/.gazebo/models/"

def get_absolute_model_pose(name):
    state = __get_model_state(name, "world")
    return state.pose

def spawn_model(name, pose, reference_frame):
    world =__get_world_properties.call()
    if name in world.model_names:
        try:
            __delete_model(name)
        except:
            rospy.logerr("Failed to delete model " + name)
    try:
        new_model_name = 'cricket_ball'
        sdf = None
        res = None

        rospy.loginfo(__path_to_models + new_model_name + "/model.sdf")
        with open(__path_to_models + new_model_name + "/model.sdf", "r") as model:
            sdf = model.read()

        res = __spawn_model(name, sdf, "", pose, reference_frame)
    except:
        rospy.logerr(res)

ball_pose = get_absolute_model_pose("cricket_ball")
sgs = SmartGrasper()
tip_pose = sgs.get_tip_pose()
tip_pose.position = ball_pose.position
tip_pose.position.z += 0.1

import pdb; pdb.set_trace()
# pose.position.x = 0.15
pose = Pose()
pose.position.z = 0.8
pose.position.y = 0.5
spawn_model("cricket_ball", pose, "google_table__table")


import pdb; pdb.set_trace()
