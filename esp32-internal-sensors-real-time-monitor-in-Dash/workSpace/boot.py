





# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

#import webrepl

#webrepl.start()
"""import the Pin class from the machine module 
to be able to interact with the GPIOs"""
from machine import Pin

import esp
"""turn off vendor OS debugging messages"""
esp.osdebug(None)

"""run a garbage collector::
A garbage collector is a form of automatic
memory management. This is a way to reclaim 
memory occupied by objects that are no longer 
in used by the program. This is useful to 
save space in the flash memory."""
import gc

"""Define some functions"""

def flash(n):
  import time
  """Create a Pin object called led that is 
an output, that refers to the ESP32/ESP8266 GPIO2:"""  
  led = Pin(25, Pin.OUT)
  for i in range(n):
    led.value(1)
    time.sleep(0.25)
    led.value(0)
    time.sleep(0.25)

def wifi(ssid,password):
  """Create web server using sockets and the Python socket API"""
  try:
    import usocket as socket
  except:
    import socket
  """The network library allows us to connect 
  the ESP32 or ESP8266 to a Wi-Fi network"""
  import network
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
 
 
def hallSensor(number_of_measurements,frequency): 
  from machine import I2C, Pin
  import esp32
  import time
  """The library to write to the OLED display isn閳ユ獩 
  part of the standard MicroPython library by default. 
  So, you need to upload the library to your ESP32/ESP8266 board. """
  import ssd1306 
  
  oled_rst = Pin(16, Pin.OUT)
  oled_rst.value(1)

  esp32.hall_sensor() #Measure Hall effect

  # ESP32 Pin assignment
  i2c = I2C(-1, Pin(15), Pin(4))
  #Configure your OLED display using the appropiate pixel resolution
  oled_width = 128
  oled_height = 64
  text_row=[]
  for n in range(7):
    text_row.append(n*10+4) #this will give you 6 lines with the default text size. print(text_row[n])
  #Create a display object where you will drwa your shapes. 
  display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
  #Optional: Set all pixels off
  display.fill(0)
  #Vertically centered text
  display.text('Hall', 19,text_row[2])
  display.text('Effect',19,text_row[3])
  display.show()


  #the esp32 is just too slow to execute this function
  """
    def displayText(string1,string2):
  
    def __init__():
      string1=''
      string2=''
  
    i2c = I2C(-1, Pin(15), Pin(4))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.fill(0)
    #Set the appropiate parameters for x,y coordinated according to font size
    display.text(str(string1), 0,5)
    display.text(str(string2), 0,15)
    display.show()
"""  
  def getInternalTemperature():
    temp = round(((( esp32.raw_temperature() - 32) / 1.8)), 1)
    return temp
    
  
#Calibrate the sensor to neglect local magnestism
  def detect_magnetism():
  
    i=0
    local_magnetism=[]
    while i<1000:
      i+=1
      time.sleep_ms(0) 
      local_magnetism.append(esp32.hall_sensor())
  
      #print(local_magnetism,'\n')
    m_avg=sum(local_magnetism) / len(local_magnetism)
    print('Local magnetism measure =',m_avg)
    return m_avg,local_magnetism

  m_avg,local_magnetism=detect_magnetism()
  
  #Set high-low filter boundary values
  high=round(max(local_magnetism),2)
  low=round(min(local_magnetism),2)
  
  #Activate sensor readings
  i=0
  j=0
  while i<number_of_measurements:
    i+=1
    time.sleep(frequency) 
    
    if esp32.hall_sensor() > high or esp32.hall_sensor() < low:
      j+=1
      temp=getInternalTemperature()
      print(1,temp) #it seems the integrated hall sensor has high variance
      
      for n in range(80,120):
        for m in range(25,45):
          display.pixel(n,m,0)
      display.text(str(j), 90,text_row[3])
      display.show()

    else:
      print(0,temp)
      
    print
    

"""    
Execute or Stop program(s) with some name, i.e. "program.py" 
"""

"""ESP32 GPIO for PRG button is at Pin 0, 
lets give this Pin object a name"""
prg = Pin(0,Pin.IN)






