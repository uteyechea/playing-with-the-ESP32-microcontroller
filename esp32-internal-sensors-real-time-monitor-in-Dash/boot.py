
import esp
import esp32
from machine import I2C,Pin #import the Pin class from the machine module to be able to interact with the GPIOs
import time
import gc #Garbage collector
try: #Create web server using sockets and the Python socket API
  import usocket as socket
except:
  import socket
import network #The network library allows us to connect the ESP32 or ESP8266 to a Wi-Fi network
"""The library to write to the OLED display isn鈥檛 part of the standard MicroPython library by default. So, you need to upload the library to your ESP32/ESP8266 board. """
import ssd1306 
from math import log    
  



esp.osdebug(None) #turn off vendor OS debugging messages

#Configure GPIOs
led = Pin(25, Pin.OUT) #Board LED (dtype PIN object)
prg = Pin(0,Pin.IN) 
#Configure oled display
# ESP32 Pin assignment
i2c = I2C(-1, Pin(15), Pin(4))
#Configure your OLED display using the appropiate pixel resolution
oled_width = 128
oled_height = 64
#display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)



"""Define some functions"""

def flash(n,led,frequency):
  for i in range(n):
    led.value(1)
    time.sleep(frequency)
    led.value(0)
    time.sleep(frequency)

def wifi(ssid,password):
  """Input variables hold your network credentials"""
  """Set the ESP32 or ESP8266 as a Wi-Fi station"""
  station = network.WLAN(network.STA_IF)
  """Activate the station"""
  station.active(True)
  """the ESP32/ESP8266 connects to your router 
  using the SSID and password defined earlier:"""
  station.connect(ssid, password)
  """The following statement ensures that you 
  get an error if the ESP is not 
  connected to your network."""
  if station.isconnected() == False:
    print('ESP is not connected to your network:\nVerify Wi-Fi network settings in boot.py ')
    print(station.ifconfig())
    flash(1)
  else:  

    print('Connection successful')
    print(station.ifconfig())
    flash(2)
 
 
def textRows(): 
  text_row=[]
  for n in range(7):
    text_row.append(n*10+4) #this will give you 6 lines with the default text size. print(text_row[n])
  return text_row
  

def getInternalTemperature():
  temp = round(((( esp32.raw_temperature() - 32) / 1.8)), 1)
  return temp
    
  
#Calibrate the sensor to neglect local magnestism
def calibrateHallSensor():  
  
  local_magnetism=[]
  for i in range(1000): #Why 1000? idk just some big random number
      #time.sleep_ms(0) #Set calibration frequency
      local_magnetism.append(esp32.hall_sensor())
  #Set high-low filter boundary values
  local_magnetism_high=round(max(local_magnetism),2)
  local_magnetism_low=round(min(local_magnetism),2)
  return local_magnetism_high,local_magnetism_low

  
  


def measureLocalMagnetism(number_of_measurements,frequency,led=led):  
  local_magnetism_high,local_magnetism_low=calibrateHallSensor()
  i=0
  while i<number_of_measurements:
    i+=1
    time.sleep(frequency) 
    #Start internal esp32 sensors measurements
    local_magnetism= esp32.hall_sensor()
    temp=getInternalTemperature()
    #Check if local_magnetism passes high-low filter
    if local_magnetism > local_magnetism_high:
      print(local_magnetism-local_magnetism_high,temp) #it seems the integrated hall sensor has high variance
      flash(3*log(local_magnetism),led,0.02)
    elif local_magnetism < local_magnetism_low:
      print(local_magnetism-local_magnetism_low,temp)
      flash(3*log(local_magnetism),led,0.02)
    else:
      print(0.0,temp)












