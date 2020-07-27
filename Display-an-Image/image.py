#!/usr/bin/env python
# coding: utf-8



from machine import I2C, Pin
import ssd1306
import framebuf

rst = Pin(16, Pin.OUT)
rst.value(1)


i2c = I2C(-1, Pin(15), Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)



display.fill(0)
display.show()

"""A file with the PBM file extension is a Portable Bitmap Image file. 
These files are text-based, black and white image files that contain either a 1 
for a black pixel or a 0 for a white pixel."""

"""#You actually need to scale the image to a resolution that your display can render,
#then export the file to a .pbm extension. You may use GIMP to accomplish this image
#pre-processing."""

with open('mouse.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
    
"""FrameBuffer 
This module provides a general frame buffer which can be used to create bitmap images, 
which can then be sent to a display."""    

 #set parameters equal to the resolution of your pbm image data.
fbuf = framebuf.FrameBuffer(data, 91, 64, framebuf.MONO_HLSB)

#invert pixel on/off behaviour
display.invert(0)
display.framebuf.blit(fbuf, 0, 0)
display.show()




