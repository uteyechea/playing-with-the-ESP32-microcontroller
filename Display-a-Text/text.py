from machine import I2C, Pin
import ssd1306

rst = Pin(16, Pin.OUT)
rst.value(1)


i2c = I2C(-1, Pin(15), Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


display.fill(0)
#Set the appropiate parameters for x,y coordinated according to font size
display.text("Hello", 0,5)
display.text("World!", 0,15)
display.show()
