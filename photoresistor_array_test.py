#!/usr/bin/python
# Python Code used for testing a photoresistor_array circuit in LTSpice by rewriting the netlist file with new
# parameters, running the netlist in LTSpice, and interpreting the output
import re
import os

def find_param_equals(parameter,line):
    """finds the parameter and value for a given line and parameter"""
    regex_string = "{} *= *\S+".format(parameter)
    param_regex = re.compile(regex_string,re.IGNORECASE)
    param_find = param_regex.findall(line)
    if param_find != []:
        param_find = param_find[0].split("=")
        param_equals = param_find[1].replace(" ","")
        return(param_equals)
    else:
        return(False)

class original_line_class:
    """container class for carrying around line and line numbers"""
    def __init__(self,line,line_number):
        self.line = line
        self.number = line_number

def process_file(filename,parameter_header_name):
    """Reads the .net file and picks out the parameters one is interested in"""
    file = open(filename,"r")
    original_file = []
    parameter_lines = []
    lines = file.readlines()
    line_count = 0
    param_line = False
    for line in lines:
        line=line[:-2]
        original_line = original_line_class(line,line_count)
        original_file.append(original_line)
        if parameter_header_name in line:
            if "End" in line:
                end_param_statement = line
                param_line = False
                parameter_lines.append(original_line)
            else:
                start_param_statement = line
                param_line = True
        if param_line == True:
            parameter_lines.append(original_line)
        line_count += 1 
    file.close()
    return(original_file,parameter_lines)

class param_statement_class:
    def __init__(self,original_line,original_param_equals):
        self.original_line = original_line
        self.param_equals = original_param_equals
    
    def replace_param_equals(self,new_param_equals,current_file_list):
        current_line = current_file_list[self.original_line.number]
        new_line = current_line.line.replace(self.param_equals,new_param_equals)
        new_line = original_line_class(new_line,self.original_line.number)
        current_file_list[self.original_line.number] = new_line
        return(current_file_list)

def switch_param_equals(change_params,original_file_list,parameter_lines):
    """Switches parameter equals in the old file with the new given parameters.
        change parameters are given as list in the format (parameter,new_equals)"""
    current_file_list = original_file_list
    for line in parameter_lines:
        for change_param in change_params:
            if change_param[0] in line.line: 
                orig_param_equals = find_param_equals(change_param[0],line.line)
                if orig_param_equals != False:
                    param_statement = param_statement_class(line,orig_param_equals)
                    param_statement.replace_param_equals(change_param[1],current_file_list)
    return(current_file_list)


def change_params_and_write_new_file(change_params,original_file_list=original_file_list,parameter_lines=parameter_lines,filename=filename):
    """Writes the new .net file so it is ready to run"""
    new_filename = filename[:-4]+"_new"+".net"
    file = open(new_filename,"w")
    print(new_filename)
    current_file_list = switch_param_equals(change_params=change_params,original_file_list=original_file_list,parameter_lines=parameter_lines)
    for line in current_file_list:
        file.write(line.line+"\n")
    file.close()
    new_filename = new_filename.split("LTspiceIV/")[-1]
    print(new_filename)
    return(new_filename)

def run_netlist(filename):
    """Runs the given netlist assuming the netlist is in the LTspiveIV directory"""
    command = "run_netlist.sh {}".format(filename)
    os.system(command)

filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Array.net"
parameter_header_name = "Resistance Parameters"
return_values = process_file(filename,parameter_header_name)
original_file_list = return_values[0]
parameter_lines = return_values[1]

change_params = [("R01","5k"),("R11","10k")]

new_filename = change_params_and_write_new_file(change_params)
run_netlist(new_filename)
