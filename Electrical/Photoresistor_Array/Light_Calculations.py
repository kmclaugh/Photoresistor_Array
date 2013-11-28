#!/usr/bin/python
import math
from python_ltspice_tools import *

#Unkown
## Ev = Illuminance seen from the LDR

## Given:
## Iv = Luminous Intensity from LED datasheet in cd/mm^2
## y = distance between LED center plane and LDR top plane in mm
## x = distance between LED perpendicular and LDR center in mm
## Aview = Viewing Angle of the LED from LED datasheet in degrees
## Lflux = Luminous Flux emitting from the LED in cd*sr

def Iv_to_Ev(Iv,x,y):
    """Convert the Luminous Intensity of the LED to the Illuminance seen by the LDR"""
    x = x * .001
    y = y * .001
    term2 = float(x/(pow(x,2) + pow(y,2))) 
    Ev = Iv * term2
    return(Ev)

def Lflux_to_Ev(Lflux,Aview,x,y):
    """Convert the Luminous Flux of the LED to the Illuminance seen by the LDR"""
    x = x * .001
    y = y * .001
    denominator1 = float(2*math.pi) * (1 - math.cos(Aview/2))
    term1 = float(Lflux)/denominator1
    
    term2 = float(x)/float(pow(x,2) + pow(y,2))

    Ev = term1 * term2

    return(Ev)


Iv = .1
#!/usr/bin/python
import math
from python_ltspice_tools import *

#Unkown
## Ev = Illuminance seen from the LDR

## Given:
## Iv = Luminous Intensity from LED datasheet in cd/mm^2
## y = distance between LED center plane and LDR top plane in mm
## x = distance between LED perpendicular and LDR center in mm
## Aview = Viewing Angle of the LED from LED datasheet in degrees
## Lflux = Luminous Flux emitting from the LED in cd*sr

def Iv_to_Ev(Iv,x,y):
    """Convert the Luminous Intensity of the LED to the Illuminance seen by the LDR"""
    x = x * .001
    y = y * .001
    term2 = float(x/(pow(x,2) + pow(y,2))) 
    Ev = Iv * term2
    return(Ev)

def Lflux_to_Ev(Lflux,Aview,x,y):
    """Convert the Luminous Flux of the LED to the Illuminance seen by the LDR"""
    x = x * .001
    y = y * .001
    denominator1 = float(2*math.pi) * (1 - math.cos(Aview/2))
    term1 = float(Lflux)/denominator1
    
    term2 = float(x)/float(pow(x,2) + pow(y,2))

    Ev = term1 * term2

    return(Ev)


Iv = .1
Lflux = None
Aview = 125
x = 10 #mm
y = 10 #mm

if Iv != None:
    Ev = Iv_to_Ev(Iv,x,y)
elif Lflux != None:
    Ev = Lflux_to_Ev(Lflux,Aview,x,y)

variable_value_dictionary = {"lux0_0":Ev}

original_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Test.net"
original_netlist = netlist_class(original_filename)
new_netlist = original_netlist.change_parameters(variable_value_dictionary)
raw_values = new_netlist.run_netlist()
read0 = raw_values.return_node_value("read0")
print("Iv = {} cd".format(Iv))
print(read0)

Lflux = None
Aview = 125
x = 10 #mm
y = 10 #mm

if Iv != None:
    Ev = Iv_to_Ev(Iv,x,y)
elif Lflux != None:
    Ev = Lflux_to_Ev(Lflux,Aview,x,y)

variable_value_dictionary = {"lux0_0":Ev}

original_filename = "/home/kevin/.wine/drive_c/Program Files/LTC/LTspiceIV/Photoresistor_Array/Photoresistor_Test.net"
original_netlist = netlist_class(original_filename)
new_netlist = original_netlist.change_parameters(variable_value_dictionary)
raw_values = new_netlist.run_netlist()
read0 = raw_values.return_node_value("read0")
print("Iv = {} cd".format(Iv))
print(read0)

