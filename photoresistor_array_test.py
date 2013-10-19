#!/usr/bin/python
# Python Code used for testing a photoresistor_array circuit in LTSpice by rewriting the netlist file with new
# parameters, running the netlist in LTSpice, and interpreting the output
import re
import os
import itertools
from python_ltspice_tools import *

def make_photoresitor_array_values(Photoresistor_Array_Values):
    """Turns a dictionary of photoresistors values into a list of params ready for simulation"""
    pr_list = []
    for key, value in Photoresistor_Array_Values.iteritems():
        if value == 1:
            value = "{Rlight}"
        elif value == 0:
            value = "{Rdark}"
        this_pair = (key,value)
        pr_list.append(this_pair)
    return(pr_list)

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

def make_voltage_cycle_array_values(on_voltage,number_of_controls):
    """Given the one control voltage integer that should be turns on, this returns the list of voltage
        parameters with all but the given voltage turned off"""
    v_param_list = []
    for v in range(0,number_of_controls):
        vparam_name = "vcon" + str(v)
        if v == on_voltage:
            vvalue = 5
        else:
            vvalue = -5
        v_param_list.append((vparam_name,str(vvalue)))
    return(v_param_list)

#----------------------------------------Results Class----------------------------------------#{{{1
class result_class:
    """A container class for a test resuts"""
    def __init__(self,name,variable_values_list,parameter_conditions_list,test_netlist,on_voltage,pass_fail=None):
        self.name=name
        self.variable_values_list = variable_values_list
        self.parameter_conditions_list = parameter_conditions_list
        self.pass_fail = pass_fail
        self.netlist = test_netlist
        self.on_voltage = on_voltage
    def __repr__(self):
        return("{}: {}".format(self.name,self.pass_fail))
    def __str__(self):
        return("{}: {}".format(self.name,self.pass_fail))

    def print_vairable_values(self):
        for variable_value in self.variable_values_list:
            print(variable_value)
#----------------------------------------END Results Class----------------------------------------#}}}

#----------------------------------------One Cylce Photoresitor Array Test----------------------------------------#{{{1
def one_cycle_photoresitor_test(photoresistor_array,array_size,original_file_list,resistor_parameter_lines,
                                voltage_parameter_lines,original_filename,test_number=0):
    """Runs the photoresistor test for the given resistor array parameters.
        Cycles through the voltages and reads the output"""
    #change resistor values
    photorestitor_params = make_photoresitor_array_values(Photoresistor_Array_Values=photoresistor_array)
    current_file_list = switch_param_equals(photorestitor_params,original_file_list,resistor_parameter_lines)
    
    results = []
    #cyle voltages, run, and colelct results
    v_controls = array_size[0] #the number of voltages to turn on
    for v in range(0,v_controls):
        test_name = str(test_number) + "." + str(v)
        print("test number: {}".format(test_name))
        
        this_v_params = make_voltage_cycle_array_values(on_voltage=v,number_of_controls=v_controls)
        current_file_list = switch_param_equals(this_v_params,current_file_list,voltage_parameter_lines)
        
        #run the file
        new_net_filenames = write_new_net_file(current_file_list=current_file_list,original_filename=original_filename)
        new_net_filename_linux = new_net_filenames[0]
        new_net_filename_wine = new_net_filenames[1]
        run_netlist(new_net_filename_wine)
        print(" ")

        #read results
        raw_filename = new_net_filename_linux.replace(".net",".raw")
        variable_values =  read_variables(raw_filename)
        this_result = result_class(name=test_name,variable_values_list=variable_values,parameter_conditions_list=[photorestitor_params,this_v_params],
                                    test_netlist=current_file_list,pass_fail=None,on_voltage="vcon"+str(v))
        results.append(this_result)
    
    return(results)
#----------------------------------------END One Cylce Photoresitor Array Test----------------------------------------#}}}

def pull_variable_type(variable_value_list,variable_base_name,unit_type):
    """Pulls the all variables of the given type out of the list. for instance:
        variable_base_name="R" and unit_type="V" would return all resistor voltage values"""
    selected_variable_list = []
    for variable_value in variable_value_list:
        if variable_base_name in variable_value.variable:
            if variable_value.unit == unit_type:
                selected_variable_list.append(variable_value)
    return(selected_variable_list)


def interpret_result(result):
    """Determines if the result behaves as expected or not"""
    #pull voltages
    Vcons = pull_variable_type(variable_value_list=result.variable_values_list,variable_base_name="vcon",unit_type="V")
    for Vcon in Vcons:
        if Vcon.variable == result.on_voltage:
            if Vcon.value != 5.0:
                print("error with test {} turn on voltage {}".format(result.name,Vcon.variable))
        else:
            if Vcon.value != -5.0:
                print("error with test {} turn off voltage {}".format(result.name,Vcon.variable))


#process original file and get resistor and voltage parameters
net_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Array.net"
original_file_list = process_file(net_filename)
resistor_parameter_header_name = "Resistance Parameters"
resistor_parameter_lines = read_parameter_lines(original_lines_list=original_file_list,parameter_header_name=resistor_parameter_header_name)
voltage_parameter_header_name = "Voltage Parameters"
voltage_parameter_lines = read_parameter_lines(original_lines_list=original_file_list,parameter_header_name=voltage_parameter_header_name)

#Make photoresistor array values
array_size = (2,2)
combinations = max_16_combinations(array_size)
Photoresistor_Array_Values = make_binary_string_values(binary_string=combinations[-1],array_size=array_size,base_param_name="R")

#Run photoresitor test
results = one_cycle_photoresitor_test(photoresistor_array=Photoresistor_Array_Values,array_size=array_size,original_file_list=original_file_list,
                    resistor_parameter_lines=resistor_parameter_lines,voltage_parameter_lines=voltage_parameter_lines,
                    original_filename=net_filename,test_number=1)

for result in results:
    result = interpret_result(result)

