def hallSensor(number_of_measurements,frequency): 
  from machine import I2C, Pin
  import esp32
  import time
  """The library to write to the OLED display isn’t 
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
      print(i,1) #it seems the integrated hall sensor has high variance
      
      for n in range(80,120):
        for m in range(25,45):
          display.pixel(n,m,0)
      display.text(str(j), 90,text_row[3])
      display.show()

    else:
      print(i,0)

