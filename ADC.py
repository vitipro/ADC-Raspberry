#!/usr/bin/env python
#
# Bitbang'd SPI interface with an MCP3008 ADC device
# MCP3008 is 8-channel 10-bit analog to digital converter
#  Connections are:
#     CLK => SCLK  
#     DOUT =>  MISO
#     DIN => MOSI
#     CS => CE0
# ref -> http://raspberrypi-aa.github.io/session3/spi.html

import time
import sys
import spidev
import argparse
import os

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000
file_name = "results.log"
curr_directory = os.path.dirname(os.path.realpath(__file__))

file_name = os.path.join(curr_directory, file_name)
f = open(file_name, "a")


def buildReadCommand(channel):
    """
    * es podria utilitzar el parametre channel per fer una funcio generica si es vol usar channels diferents
    """
    startBit = 0x06
    singleEnded = 0x00

    # Return python list of 3 bytes
    #   Build a python list using [1, 2, 3]
    #   First byte is the start bit
    #   Second byte contains single ended along with channel #
    #   3rd byte is 0
    return [startBit, singleEnded, 0]
    
def processAdcValue(result):
    '''Take in result as array of three bytes. 
       Return the two lowest bits of the 2nd byte and
       all of the third byte'''
    return ((result[1] & 0b00001111) << 8) + result[2]
    pass
        
def readAdc(channel):
    if ((channel > 7) or (channel < 0)):
        return -1
    r = spi.xfer2(buildReadCommand(channel))
    return processAdcValue(r)

def read_values(num_values:int)->int:
    avg = 0
    try:
        for i in range(num_values):
            avg += readAdc(0)
            time.sleep(0.02)
    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
        return -1
    avg /= num_values
    return avg
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--input_voltage",help="voltatge d'entrada de l'experiment")
    args = parser.parse_args()
    f.write("Voltatge: " + args.input_voltage + "\n")
    f.write(str(read_values(100))+"\n")
    f.close()
   
