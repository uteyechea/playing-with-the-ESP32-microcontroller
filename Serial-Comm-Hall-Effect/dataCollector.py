#!/usr/bin/env python
# coding: utf-8

# ### install pySerial using pip or whatever you use. 
# pip install pySerial

# In[59]:


import serial


# In[71]:


ser=serial.Serial('COM4',baudrate=115200,timeout=1)


# In[ ]:


while 1:
    arduinoData = ser.readline().decode('ascii')
    print('Hall effect counter, 0: No magnetism, 1:Magnetism')
    print('Magnetism Detected ',arduinoData)


# In[ ]:


ser.close()


# In[ ]:




