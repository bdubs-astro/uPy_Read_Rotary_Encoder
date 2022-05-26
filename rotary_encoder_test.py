'''
Tests a class used to read a KY-040 rotary encoder using interrupts.

Resources:
https://github.com/gurgleapps/rotary-encoder
https://gurgleapps.com/learn/electronics/ky-040-rotary-encoder-on-a-raspberry-pi-pico-detailed-explanation-and-step-by-step-code
'''

from rotary_bdw import Rotary
import utime as time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf

rotary = Rotary(16,17,18)  # pin numbers: clk,dt,sw
val = 0

# I2C OLED setup
from micropython import const
oledSDA = const(4)
oledSCL = const(5)
WIDTH  = 128                                          
HEIGHT = 32    
i2c = I2C(0, scl=Pin(oledSCL), sda=Pin(oledSDA), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, 0x3C)

'''
enable larger fonts for the OLED display
https://github.com/peterhinch/micropython-font-to-py
https://www.youtube.com/watch?v=bLXMVTTPFMs
https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-vi-working-with-a-screen
'''
import writer
import freesans20

def dispStr (x, y, str, dispLogo = True):
    # Raspberry Pi logo as 32x32 bytearray
    logo = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
     
    oled.fill(0)
    font_writer = writer.Writer(oled, freesans20, False) # disable verbose mode
    font_writer.set_textpos(x, y)
    font_writer.printstring(str)
    if dispLogo:
        fb = framebuf.FrameBuffer(logo, 32, 32, framebuf.MONO_HLSB)  # load the framebuffer
        # MONO_HLSB: monochrome, horizontally mapped - each byte occupies 8 horizontal pixels with bit 0 being the leftmost 
        oled.blit(fb, 96, 0) # blit the image from the framebuffer to the display
    oled.show()
    
def rotary_changed(event):
    global val
    if event == Rotary.ROT_CW:
        val +=  1
        print(val)
    elif event == Rotary.ROT_CCW:
        val -= 1
        print(val)
    elif event == Rotary.SW_PRESS:
        print('Switch Pressed')
    elif event == Rotary.SW_RELEASE:
        print('Switch Released')
        val = 0 # reset position
        print(val)
            
    # display results on OLED ...
    dispStr (5, 5, ('%d' %(val)))
    
rotary.add_handler(rotary_changed)

while True:
    time.sleep_ms(10)
