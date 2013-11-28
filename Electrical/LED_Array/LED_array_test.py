#!/usr/bin/python
# Python Code used for testing a photoresistor_array circuit in LTSpice by rewriting the netlist file with new
# parameters, running the netlist in LTSpice, and interpreting the output
import re
import os
import itertools
import copy
import datetime
from python_ltspice_tools import *

def find_current(netlist,on_LED):
    """Finds the current of the turned on LED"""
    raw_results = netlist.run_netlist()
    current = raw_results.return_node_value("LED1_1","device")
    return(current)

def find_luminous_intensity(current):
    """Finds the luminous intensity corresponding to the given current (in Amps) as determined
        by the line given on the datasheet rv = 0.05 c"""
    
    compare_value = 400 #mcd
    
    current = 1000 * current 
    relative_value = 0.05 * current
    luminous_intensity = relative_value * compare_value

    return(luminous_intensity)


def Iv_to_Ev(Iv,x,y):
    """Convert the Luminous Intensity of the LED to the Illuminance seen by the LDR"""
    term2 = float(x/(pow(x,2) + pow(y,2))) 
    Ev = Iv * term2
    return(Ev)

x = 1000 #mm
y = 10 #mm
#Convert mm to m
x = x * .001
y = y * .001
    
#Filenames
original_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/LED_Array/LED_Array_Small.net"

#process original file, run it, and get the LED's current 
original_netlist = netlist_class(original_filename)
on_LED = "LED1_1"
current = find_current(netlist=original_netlist, on_LED=on_LED)
current = current.values[0]

luminous_intensity = find_luminous_intensity(current)
luminous_intensity = luminous_intensity * .001 #convert mcd to c
Ev = Iv_to_Ev(Iv=luminous_intensity,x=x,y=y)
variable_value_dictionary = {"lux0_0":Ev}

original_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Test.net"
original_netlist = netlist_class(original_filename)
new_netlist = original_netlist.change_parameters(variable_value_dictionary)
raw_values = new_netlist.run_netlist()
read0 = raw_values.return_node_value("read0")

print("Id = {} mA".format(current*1000))
print("Iv = {} mcd".format(luminous_intensity))
print("Ev = {} lux".format(Ev))
print(read0)

