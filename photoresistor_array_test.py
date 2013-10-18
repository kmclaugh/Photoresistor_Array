#!/usr/bin/python
# Python Code used for testing a photoresistor_array circuit in LTSpice by rewriting the netlist file with new
# parameters, running the netlist in LTSpice, and interpreting the output
import re
import os
import itertools
from python_ltspice_tools import *

def make_binary_string_values(binary_string,array_size,base_param_name):
    """converts a binary string to an photorestor array values dictionary."""
    x_total = array_size[0]
    y_total = array_size[1]
    array = []
    for y in range(0,y_total):
        row = []
        for x in range(0,x_total):
            param_name = base_param_name + str(x) + str(y)
            row.append(param_name)
        array.append(row)
    photoresistor_array = {}
    binary_count = 0
    row_count = 0
    while row_count <= y_total-1:
        if row_count + 1 <= y_total-1:
            for xy0,xy1 in zip(array[row_count],array[row_count+1]):
                photoresistor_array[xy0] = int(binary_string[binary_count])
                binary_count += 1
                photoresistor_array[xy1] = int(binary_string[binary_count])
                binary_count += 1
        else:
            for xy0 in array[row_count]:
                photoresistor_array[xy0] = int(binary_string[binary_count])
                binary_count += 1
        row_count += 2
    return(photoresistor_array)

def make_specific_test(array_values,base_param_name):
    """convert an array of rows into a photoresistor array"""
    x_total = len(array_values[0])
    y_total = len(array_values)
    array_names = []
    for y in range(0,y_total):
        row = []
        for x in range(0,x_total):
            param_name = base_param_name + str(x) + str(y)
            row.append(param_name)
        array_names.append(row)
    photoresistor_array = {}
    for row_name,row_value in zip(array_names,array_values):
        for name,value in zip(row_name,row_value):
            photoresistor_array[name]=value
    return(photoresistor_array)
    
def make_array_values(Photoresistor_Array_Values):
    """Turns a dictionary of photoresistors values into a list of params ready for simulation"""
    pr_list = []
    for key, value in Photoresistor_Array_Values.iteritems():
        if value == 1:
            value = "{Rligt}"
        elif value == 0:
            value = "{Rdark}"
        this_pair = (key,value)
        pr_list.append(this_pair)
    return(pr_list)

def all_combinations(array_size):
    """returns a list of binary strings that represent all possible combinations for the resistors.
        given the size of the array as a tuple (X,Y)."""
    total_resistors = array_size[0]*array_size[1]
    all_combos = ["".join(seq) for seq in itertools.product("01", repeat=total_resistors)]
    return(all_combos)

def max_16_combinations(array_size):
    """returns a list of binary string for a given array size of the first 16 possible combos.
        This corresponds to a 4x4 array which is theoretically the maximum size where one photoresistor
        could affect the other."""
    total_resistors = array_size[0]*array_size[1]
    all_combos = []
    total_count = 0
    for seq in itertools.product("01", repeat=total_resistors):
        if total_count > 15:
            break
        this_value = "".join(seq)
        all_combos.append(this_value)
        total_count += 1
    return(all_combos)



array_size = (2,2)
combinations = max_16_combinations(array_size)
quad_test = [[1,1],[1,0]]
quad_test = make_specific_test(quad_test,"R")
print(quad_test)
Photoresistor_Array_Values = make_photoresistor_array_values(combinations[-1],array_size,"R")

#process original file
net_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Array.net"
parameter_header_name = "Resistance Parameters"
return_values = process_file(net_filename,parameter_header_name)
original_file_list = return_values[0]
parameter_lines = return_values[1]

#change parameters, create and run new file
change_params = make_array_values(Photoresistor_Array_Values)
current_file_list = switch_param_equals(change_params,original_file_list,parameter_lines)
new_net_filenames = write_new_net_file(current_file_list,original_filename=net_filename)
new_net_filename_linux = new_net_filenames[0]
new_net_filename_wine = new_net_filenames[1]
#run_netlist(new_net_filename_wine)

#read results
raw_filename = new_net_filename_linux.replace(".net",".raw")
variable_values =  read_variables(raw_filename)
#for variable in variable_values:
#    print(variable)


