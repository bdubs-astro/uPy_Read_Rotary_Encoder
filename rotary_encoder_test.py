'''
Tests a class used to read a KY-040 rotary encoder using interrupts.

Resources:

rotary encoder:
https://github.com/gurgleapps/rotary-encoder
https://gurgleapps.com/learn/electronics/ky-040-rotary-encoder-on-a-raspberry-pi-pico-detailed-explanation-and-step-by-step-code

larger fonts for the OLED display:
https://github.com/peterhinch/micropython-font-to-py
https://www.youtube.com/watch?v=bLXMVTTPFMs
https://blog.miguelgrinberg.com/post/micropython-and-the-internet-of-things-part-vi-working-with-a-screen
'''

from rotary_bdw import Rotary
import utime as time
from micropython import const

def disp_setup(scl_pin, sda_pin, width, height, id = 0, addr = 0x3C):
    from machine import Pin, I2C
    from ssd1306 import SSD1306_I2C
    
    i2c = I2C(id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr)
    return oled

def disp_string (oled, x, y, str, disp_logo = True):
    import framebuf
    import writer
    import freesans20

    # Raspberry Pi logo as 32x32 bytearray
    logo = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
     
    oled.fill(0)
    font_writer = writer.Writer(oled, freesans20, False) # disable verbose mode
    font_writer.set_textpos(x, y)
    font_writer.printstring(str)
    if disp_logo:
        fb = framebuf.FrameBuffer(logo, 32, 32, framebuf.MONO_HLSB)  # load the framebuffer
        # MONO_HLSB: monochrome, horizontally mapped - each byte occupies 8 horizontal pixels with bit 0 being the leftmost 
        oled.blit(fb, 96, 0) # blit the image from the framebuffer to the display
    oled.show()
    
def rotary_event(event):
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
            
    # display results ...
    disp_string (oled, 5, 5, ('%d' %(val)))


# rotary endcoder setup
rotary = Rotary(16,17,18)  # pin numbers: clk,dt,sw
rotary.add_handler(rotary_event)
val = 0

# I2C OLED setup
scl_pin= const(5)
sda_pin = const(4)
WIDTH  = 128                                          
HEIGHT = 32  
oled = disp_setup(scl_pin, sda_pin, WIDTH, HEIGHT)

# display initial reading
disp_string (oled, 5, 5, ('%d' %(val)))
print(val)

while True:
    time.sleep_ms(10)
