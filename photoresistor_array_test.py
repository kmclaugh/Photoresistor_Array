#!/usr/bin/python
# Python Code used for testing a photoresistor_array circuit in LTSpice by rewriting the netlist file with new
# parameters, running the netlist in LTSpice, and interpreting the output
import re
import os
import itertools
import copy
import datetime
from python_ltspice_tools import *

#----------------------------------------Netlist-Results Class----------------------------------------#{{{1
class netlist_results_class:
    """A class containing both the netlist and resulting raw file for one run of a photoresistor array test.
        Methods for verifying the outputs match the input"""
    def __init__(self,netlist,raw_values,test_name):
        
        self.netlist= netlist
        self.raw_values = raw_values
        self.test_name = test_name

        #Dummy values to these attributes placed here for easy reference
        self.passed = "Passed"
        self.report = []
        self.error_report = []
        self.input_resistances = {} #of list of columns of resistor parameters statements
        self.vcontrols = []

        self.verify_test_routine()
 
    #----------------------------------------Verify Cycle Routine----------------------------------------#{{{2
    def verify_test_routine(self):
        """Checks that the resulting voltages correspend as expected with the resistances
            and voltages contaned in the netlist and raw_values objects. Checks that the only one input is on
            and the voltages for the output and within a given expected range based on the resistances."""
        #Test values declared outside fuction
        global Vcon_on
        global Vcon_off
        global Vread_on
        global Vread_off

        ##Collect input resistance values and makes sure only 1 Vcon is turned on
        xinput_resistances = {} #input resistances grouped by x values(columns)
        yinput_resistances = {} #input resistances grouped by y values(rows)
        vcontrols = []
        found_von = False
        for variable, parameter_statement_obj in self.netlist.parameters.iteritems():
            if "vcon" in variable:
                control_number = int(''.join(x for x in variable if x.isdigit()))
                if parameter_statement_obj.value == Vcon_on:
                    if found_von == False:
                        self.von = control_number
                        found_von = True
                    else:
                        self.passed = "Failed"
                        self.error_report.append("Error: Two Vcon were turned on")
                vcontrols.append((parameter_statement_obj,control_number))
            if "lux" in variable:
                if "load" in variable:
                    pass
                else:
                    resistor_tuple = variable.split("_")
                    resistor_x = int(''.join(x for x in resistor_tuple[0] if x.isdigit()))
                    resistor_y = int(''.join(y for y in resistor_tuple[1] if y.isdigit()))
                    #if the x value is already in the dictionary append the param statement. If makes the new xkey
                    try:
                        xinput_resistances[str(resistor_x)].append((parameter_statement_obj,resistor_y))
                    except:
                        xinput_resistances[str(resistor_x)] = [(parameter_statement_obj,resistor_y)]
                    try:
                        yinput_resistances[str(resistor_y)].append((parameter_statement_obj,resistor_x))
                    except:
                        yinput_resistances[str(resistor_y)] = [(parameter_statement_obj,resistor_x)]
        #save the inputs for the reports
        self.xinput_resistances = xinput_resistances
        self.yinput_resistances = yinput_resistances
        self.vcontrols = vcontrols

        ##Verify read voltages of the resistors connected to the Von are what they should be
        if found_von == False:
            self.passed = "Failed"
            self.error_report.append("Error: No Vcon were turned on")
        else:
            on_resistors = xinput_resistances[str(self.von)]
            for resistor in on_resistors:
                read_node = "read{}".format(resistor[1])
                
                read_node = self.raw_values.node_values[read_node]
                if resistor[0].value[0] == "100":
                    if read_node.values[0] <= Vread_on:
                        error = (resistor[0],read_node)
                        self.error_report.append(error)
                        self.passed = "Failed"
                    else:
                        report = (resistor[0],read_node)
                        self.report.append(report)
                elif resistor[0].value[0] == "0":
                    if read_node.values[0] >= Vread_off:
                        error = (resistor[0],read_node)
                        self.error_report.append(error)
                        self.passed = "Failed"
                    else:
                        report = (resistor[0],read_node)
                        self.report.append(report)
    #----------------------------------------END Verify Cycle Routine----------------------------------------#}}}

    #----------------------------------------Report File Functions----------------------------------------#{{{2
    def resistance_parameter_string(self):
        """Organizes the resitance parameters by colomun and returns a string for easy readibility"""
        
        row_format_string = ""
        column_total = len(self.xinput_resistances)
        for column in range(0,column_total):
            row_format_string += "%15s"
            
        row_total = len(self.yinput_resistances)
        string_array = []
        for row_number in range(0,row_total):
            this_row = self.yinput_resistances[str(row_number)]
            this_row = sorted(this_row, key=lambda x:x[1])
            print_row = []
            for x in this_row:
                print_row.append(x[0])
            string_array.append(print_row)

        resistor_string = ""
        for row in string_array:
            row_string = row_format_string % tuple(row)
            resistor_string += row_string + "\n"
        self.row_format_string = row_format_string
        return(resistor_string)

    def report_file_string(self):
        """generates the string to be inserted into the report"""
        final_string = "Test {} {}\n".format(self.test_name,self.passed)
        resistor_string = self.resistance_parameter_string()
        vcontrols = []
        self.vcontrols = sorted(self.vcontrols, key=lambda x:x[1])
        for vcon in self.vcontrols:
            vcontrols.append(vcon[0])
        voltage_string = self.row_format_string % tuple(vcontrols) +"\n" #this is a bad hack
        final_string += voltage_string
        final_string += resistor_string
        
        report_string = ""
        self.report = sorted(self.report, key=lambda x:int(x[1].node[4])) #this is bad hack for sorting the read line but fuck it
        for statement in self.report:
            report_string +=  str(statement[1]) + "\n"
        final_string += report_string
        
        return(final_string)
    #----------------------------------------END Report File Functions----------------------------------------#}}}
    
           

#----------------------------------------END Netlist-Results Class----------------------------------------#}}}                

#----------------------------------------Write Report----------------------------------------#{{{1
def write_report(results,report_filename,error_filename):
    """Write the report to a file in an intellegible manner"""
    report_file = open(report_filename,"w")
    error_file = open(error_filename,"w")
    error = False
    for result in results:
        print(result.test_name,result.passed)
        report_string = result.report_file_string() + "\n" 
        report_file.write(report_string)
        if result.passed == "Failed":
            error = True
            error_file.write(report_string)
    if error == True:
        print("there was an error")
    else:
        print("PASSSED!!!!!!!!!!!!!!!!!")
        error_file.write("No errors. Well done, sir")
    report_file.close()
    error_file.close()
#----------------------------------------END Write Report----------------------------------------#}}}

#----------------------------------------Make Voltage Cycle Array Values----------------------------------------#{{{1
def make_voltage_cycle_array_values(on_voltage,number_of_controls):
    """Given the one control voltage integer that should be turns on, this returns the list of voltage
        parameters with all but the given voltage turned off"""
    v_param_list = {}
    for v in range(0,number_of_controls):
        vparam_name = "vcon" + str(v)
        if v == on_voltage:
            vvalue = 5
        else:
            vvalue = -5
        v_param_list[vparam_name]=str(vvalue)
    return(v_param_list)
#----------------------------------------END make voltage cycle array value----------------------------------------#}}}

#----------------------------------------One Cylce Photoresitor Array Test----------------------------------------#{{{1
def one_cycle_photoresitor_test(photoresistor_array,array_size,netlist,base_test_name):
    """Run a single cyle of voltages with the given photoresistor values for the given array size. 
        Returns a list of the resulting the raw_values objects"""
    results = []
    netlist = netlist.change_parameters(variable_value_dictionary=photoresistor_array)
    for v in range(0,array_size[0]):
        
        this_test_name = base_test_name + "." + str(v)
        v_param_list = make_voltage_cycle_array_values(v,array_size[0])
        new_netlist = netlist.change_parameters(variable_value_dictionary=v_param_list)
        
        #Here is where the code actually runs a simulation
        print(this_test_name)
        new_raw_values = new_netlist.run_netlist()
        netlist_results = netlist_results_class(new_netlist,new_raw_values,test_name=this_test_name)
        results.append(copy.deepcopy(netlist_results))#needs to deep copy or the results class append will just be a pointer

    return(results)
#----------------------------------------END One Cylce Photoresitor Array Test----------------------------------------#}}}

#---------------------------------------- Test Creators----------------------------------------#{{{1
def make_photoresitor_array_values(Photoresistor_Array_Values):
    """Turns a dictionary of photoresistors values into a list of params ready for simulation"""
    pr_dict = {}
    for key, value in Photoresistor_Array_Values.iteritems():
        if value == 1:
            value = "100"
        elif value == 0:
            value = "0"
        else:
            value = str(value)
        pr_dict[key] = value
    return(pr_dict)

def make_binary_string_values(binary_string,array_size,base_param_name):
    """converts a binary string to an photorestor array values dictionary."""
    x_total = array_size[0]
    y_total = array_size[1]
    array = []
    for y in range(0,y_total):
        row = []
        for x in range(0,x_total):
            param_name = base_param_name + str(x)+ "_" + str(y)
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
            param_name = base_param_name + str(x) + "_" + str(y)
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

def max_combinations(array_size,max_number=16):
    """Returns a binary string list of the first possible combinations up to the max number of tests
        given"""
    total_resistors = array_size[0]*array_size[1]
    all_combos = []
    total_count = 0
    for seq in itertools.product("01", repeat=total_resistors):
        if total_count > max_number-1:
            break
        this_value = "".join(seq)
        all_combos.append(this_value)
        total_count += 1
    return(all_combos)

def combinations_test(array_size,max_number=16):
    """Runs 16 different combinations of input since all would be too long"""
    combinations = max_combinations(array_size,max_number)
    all_results = []
    test_counter = 1
    for combination in combinations:
        photoresistor_array = make_binary_string_values(binary_string=combination,array_size=array_size,base_param_name="lux")
        photoresistor_array = make_photoresitor_array_values(photoresistor_array)
        
        #Run photoresitor test
        test_name = "Combinations_Test_"+str(test_counter)
        results = one_cycle_photoresitor_test(photoresistor_array=photoresistor_array,array_size=array_size,netlist=original_netlist,
                                            base_test_name=test_name)

        all_results += results
        test_counter += 1
    return(all_results)

def all_on_test(array_size):
    """Test with all the photoresistors turned on"""
    row_value = []
    for x in range(0,array_size[0]):
        row_value.append("100")
    array_values = []
    for y in range(0,array_size[1]):
        array_values.append(row_value)
    photoresistor_array = make_specific_test(array_values,"lux")
    all_results = one_cycle_photoresitor_test(photoresistor_array=photoresistor_array,array_size=array_size,netlist=original_netlist,
                                            base_test_name="all_on_1")
    return(all_results)

def all_off_test(array_size):
    """Test with all the photoresistors turned off"""
    row_value = []
    for y in range(0,array_size[0]):
        row_value.append(0)
    array_values = []
    for x in range(0,array_size[1]):
        array_values.append(row_value)
    photoresistor_array = make_specific_test(array_values,"lux")
    all_results = one_cycle_photoresitor_test(photoresistor_array=photoresistor_array,array_size=array_size,netlist=original_netlist,
                                            base_test_name="all_off_1")
    return(all_results)
#----------------------------------------END Test Creators----------------------------------------#}}}

#Test Parameters
Vcon_on = "5"
Vcon_off = "-5"
Vread_on = 4.0 #V
Vread_off = 0.1 #V
max_combos_test = 16

#Filenames
original_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Array.net"
current_date = datetime.datetime.today()
current_date_time_string = current_date.strftime("%m-%d-%Y-%H-%M")
error_filename = "/home/kevin/Projects/Pill_Case/Design/Photoresistor_Array/Reports/error_report-{}.txt".format(current_date_time_string)
report_filename = "/home/kevin/Projects/Pill_Case/Design/Photoresistor_Array/Reports/results_report-{}.txt".format(current_date_time_string)

#process original file and get resistor and voltage parameters
original_netlist = netlist_class(original_filename)
array_size = (7,4) #in (x,y) or (vcon,read)

#Run Test Bench
all_results = all_on_test(array_size)
#all_results += all_off_test(array_size) all off is covered in combinations
all_results += combinations_test(array_size,max_combos_test)

#Write Report Files
write_report(all_results,report_filename,error_filename)
    
    
