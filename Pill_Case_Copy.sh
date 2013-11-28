#!/bin/bash
#Save directory paths
PROJECT_DIRECTORY=~/Projects/Pill_Case

############################### Photoresistor Directory ########################
PHOTO_RES_DIR=$PROJECT_DIRECTORY/Electrical/Photoresistor_Array
#Circuit Directory
cd $PHOTO_RES_DIR/Hardware/Circuit

#Moving all files with .py for preservation
find . -iname "*.py" -exec mv {} ../ \;
cd ../
#Removing all files.
rm -rfv Circuit/*

#LTSpice Files
cd "$SPICE"
cd Photoresistor_Array
#Copying current files to project directory
cp -a . $PHOTO_RES_DIR/Hardware/Circuit/
#LTSpice Files

#Diptrace Files
cd "$DIPTRACEFILES"
cd Projects/Photoresistor_Array

#Copying current files to project directory
cp -a . $PHOTO_RES_DIR/Hardware/Circuit/
#End Diptrace

#move the saved files back into the lower directory
cd $PHOTO_RES_DIR/Hardware
find . -iname "*.py" -exec mv {} Circuit \;

#Arduino Files
cd $PHOTO_RES_DIR/Code/Arduino_Code
#Moving all files with .py for preservation
find . -iname "*.py" -exec mv {} ../ \;
cd ../

#Removing all files. 
rm -rfv Arduino_Code/*
#cd to the directory with the current files
cd ~/Arduino/Photoresistor_Modules

#Copying current files to project directory
cp -a . $PHOTO_RES_DIR/Code/Arduino_Code
cd $PHOTO_RES_DIR/Code

#move the saved files back into the lower directory
find . -iname "*.py" -exec mv {} Circuit \;

#End Arduino Files 

######################END Photoresistor Array###################


############################### LED Directory ########################
LED_RES_DIR=$PROJECT_DIRECTORY/Electrical/LED_Array
#Circuit Directory
cd $LED_RES_DIR/Hardware/Circuit

#Moving all files with .py for preservation
find . -iname "*.py" -exec mv {} ../ \;
cd ../
#Removing all files.
rm -rfv Circuit/*

#LTSpice Files
cd "$SPICE"
cd LED_Array
#Copying current files to project directory
cp -a . $LED_RES_DIR/Hardware/Circuit/
#LTSpice Files

#Diptrace Files
#cd "$DIPTRACEFILES"
#cd Projects/LED_Array

#Copying current files to project directory
#cp -a . $LED_RES_DIR/Hardware/Circuit/
#End Diptrace

#move the saved files back into the lower directory
cd $LED_RES_DIR/Hardware
find . -iname "*.py" -exec mv {} Circuit \;

#Arduino Files
#cd $LED_RES_DIR/Code/Arduino_Code
#Moving all files with .py for preservation
#find . -iname "*.py" -exec mv {} ../ \;
#cd ../

#Removing all files. 
#rm -rfv Arduino_Code/*
#cd to the directory with the current files
#cd ~/Arduino/Photoresistor_Modules

#Copying current files to project directory
#cp -a . $LED_RES_DIR/Code/Arduino_Code
#cd $LED_RES_DIR/Code

#move the saved files back into the lower directory
#find . -iname "*.py" -exec mv {} Circuit \;

#End Arduino Files 

######################END LED Array###################

######################Mechanical###############################
cd $PROJECT_DIRECTORY
rm -rfv Mechanical
cd "/home/kevin/Google Drive/Projects/Pill Case/Engineering"
insync force_sync Mechanical
sleep 5
cp -avr Mechanical $PROJECT_DIRECTORY
######################END Mechanical##########################


