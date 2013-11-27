#!/usr/bin/python
import math

#Unkown
## Ev = Illuminance seen from the LDR

## Given:
## Iv = Luminous Intensity from LED datasheet in cd/mm^2
## y = distance between LED center plane and LDR top plane in mm
## x = distance between LED perpendicular and LDR center in mm
## Aview = Viewing Angle of the LED from LED datasheet in degrees
## Lflux = Luminous Flux emitting from the LED in cd*sr

Iv = None
Lflux = 29
Aview = 125
x = 10
y = 10

def Iv_to_Ev(Iv,x,y):
    """Convert the Luminous Intensity of the LED to the Illuminance seen by the LDR"""
    Ev = Iv * (x/(pow(x,2) + pow(y,2)))
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

if Iv != None:
    result = Iv_to_Ev(Iv,x,y)
elif Lflux != None:
    result = Lflux_to_Ev(Lflux,Aview,x,y)

print(result)
