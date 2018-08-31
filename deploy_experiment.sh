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
 cp google_virtuallab.sdf $HBP/Models/google_grasping_models/google_virtuallab/google_virtuallab.sdf	
fi
#
if [ "$1" = "" ] || [ "$1" = "e" ] ; then
 echo "copying experiment"
 mkdir $HBP/Experiments/GoogleGrasping
 if [ $? -ne 0 ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/Experiments/GoogleGrasping
  mkdir $HBP/Experiments/GoogleGrasping
 fi
 cp bibi_configuration.bibi $HBP/Experiments/GoogleGrasping/bibi_configuration.bibi
 cp experiment_configuration.exc $HBP/Experiments/GoogleGrasping/experiment_configuration.exc
 #cp GoogleGrasping.3ds $HBP/Experiments/GoogleGrasping/GoogleGrasping.3ds
 cp GoogleGrasping.jpg $HBP/Experiments/GoogleGrasping/GoogleGrasping.jpg
 cp GoogleGrasping.uis $HBP/Experiments/GoogleGrasping/GoogleGrasping.uis
 cp load_param.launch $HBP/Experiments/GoogleGrasping/load_param.launch
 cp idle_brain.py $HBP/Experiments/GoogleGrasping/idle_brain.py
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

