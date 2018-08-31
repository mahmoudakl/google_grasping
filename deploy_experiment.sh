#!/bin/bash  

echo "Starting to Deploy"  
git submodule init
git submodule update --recursive
echo "submodule initalized"
if [ "$1" = "" ] || [ "$1" = "g" ] ; then
 echo "copying packages"
 mkdir $HBP/GazeboRosPackages/src/google_grasping_packages
 if [ $? -ne 0 ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/GazeboRosPackages/src/google_grasping_packages
  mkdir $HBP/GazeboRosPackages/src/google_grasping_packages
 fi
 cp resources/GazeboRosPackages/* $HBP/GazeboRosPackages/src/google_grasping_packages -a
fi
#
if [ "$1" = "" ] || [ "$1" = "m" ] ; then
 echo "copying models"
 mkdir $HBP/Models/google_grasping_models
 if [ $? -ne 0 ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/Models/google_grasping_models
  mkdir $HBP/Models/google_grasping_models
 fi
 cp resources/Models/* $HBP/Models/google_grasping_models -a
 cp ur_description/model.sdf $HBP/Models/google_grasping_models/ur_description/model.sdf
 cp ur_description/google_virtuallab.sdf $HBP/Models/google_grasping_models/ur_description/google_virtuallab.sdf	
fi
#
if [ "$1" = "" ] || [ "$1" = "e" ] ; then
 echo "copying experiment"
 mkdir $HBP/Experiments/google_grasping
 if [ $? -ne 0 ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/Experiments/google_grasping
  mkdir $HBP/Experiments/google_grasping
 fi
 cp bibi_configuration.bibi $HBP/Experiments/google_grasping/bibi_configuration.bibi
 cp experiment_configuration.exc $HBP/Experiments/google_grasping/experiment_configuration.exc
 cp google_grasping_single.3ds $HBP/Experiments/google_grasping/google_grasping_single.3ds
 cp google_grasping_single.png $HBP/Experiments/google_grasping/google_grasping_single.png
 cp google_grasping_single.uis $HBP/Experiments/google_grasping/google_grasping_single.uis
 cp schunk_arm_control.py $HBP/Experiments/google_grasping/schunk_arm_control.py
 cp schunk_gripper_control.py $HBP/Experiments/google_grasping/schunk_gripper_control.py
 cp schunk_hand_control.py $HBP/Experiments/google_grasping/schunk_hand_control.py
 cp smart_grasping_sandbox.launch $HBP/Experiments/google_grasping/smart_grasping_sandbox.launch
 cp statemachine_0_1525861273136_frontend_generated.exd $HBP/Experiments/google_grasping/statemachine_0_1525861273136_frontend_generated.exd
 cp bibi_configuration.bibi $HBP/Experiments/google_grasping/bibi_configuration.bibi
fi
#
echo "done copying"
if [ "$1" = "" ] || [ "$1" = "m" ] ; then
 echo "setting up models"
 cd $HBP/Models
 ./create-symlinks.sh
fi
#
if [ "$1" = "" ] || [ "$1" = "g" ] ; then
 echo "setting up packages"
 cd $HBP/GazeboRosPackages
 catkin_make
fi

echo "Experiment succesfully deployed"

