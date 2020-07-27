#!/usr/bin/env python
# coding: utf-8


from machine import I2C, Pin
import ssd1306
import time
import framebuf

rst = Pin(16, Pin.OUT)
rst.value(1)

i2c = I2C(-1, Pin(15), Pin(4))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


images = []
for n in range(1,9):
    with open('stickman.%s.pbm' % n, 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 77, 64, framebuf.MONO_HLSB)
    images.append(fbuf)

display.invert(0)
while True:
    for i in images:
        display.framebuf.blit(i, 0, 0)
        display.show()
        time.sleep(0.1)

