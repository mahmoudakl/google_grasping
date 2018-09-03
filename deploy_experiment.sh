#!/bin/bash  

# This bash script copies the necessary files to your local NRP repositories in order
# for the experiment to be clonable and runnable on your local setup.

echo "Starting to Deploy"  
git submodule init
git submodule update --recursive
echo "submodule initalized"

# GazeboRosPackages
if [ "$1" = "" ] || [ "$1" = "g" ] ; then
 echo "copying packages"
 if [ -d "$HBP/GazeboRosPackages/src/google_grasping_packages"  ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/GazeboRosPackages/src/google_grasping_packages
 fi
 mkdir $HBP/GazeboRosPackages/src/google_grasping_packages
 cp resources/GazeboRosPackages/* $HBP/GazeboRosPackages/src/google_grasping_packages -a
fi

# Models
if [ "$1" = "" ] || [ "$1" = "m" ] ; then
 echo "copying models"
 if [ -d "$HBP/Models/google_grasping_models" ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/Models/google_grasping_models
 fi
 mkdir $HBP/Models/google_grasping_models
 cp resources/Models/* $HBP/Models/google_grasping_models -a
fi

# Experiment
if [ "$1" = "" ] || [ "$1" = "e" ] ; then
 echo "copying experiment"
 if [ -d "$HBP/Experiments/GoogleGrasping" ] ; then
  echo "overwriting existing folder" 
  rm -r $HBP/Experiments/GoogleGrasping
 fi
 mkdir $HBP/Experiments/GoogleGrasping
 cp {*.bibi,*.exc,*.json,*.jpg,*.png,*.ini,*.uis,*.launch,*.py} $HBP/Experiments/GoogleGrasping
fi
# rename experiment name to distinguish repository from cloned experiments
sed -e 's/ - Repository//g' -i $HBP/Experiments/GoogleGrasping/experiment_configuration.exc

echo "done copying"

# Create Symbolic Links for Models
if [ "$1" = "" ] || [ "$1" = "m" ] ; then
 echo "setting up models"
 cd $HBP/Models
 ./create-symlinks.sh
fi

# Re-building GazeboRosPackages
if [ "$1" = "" ] || [ "$1" = "g" ] ; then
 echo "setting up packages"
 cd $HBP/GazeboRosPackages
 catkin_make
fi

echo "Experiment successfully deployed"

