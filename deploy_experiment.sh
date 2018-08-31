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
 cp resources/Experiments/* $HBP/Experiments/google_grasping
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

