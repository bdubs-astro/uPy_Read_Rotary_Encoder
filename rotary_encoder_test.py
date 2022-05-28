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
import ssd1306_display_module as display

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
    # display encoder position
    display.disp_string (oled, 5, 5, ('%d' %(val)))


# rotary endcoder setup
rotary = Rotary(16, 17, 18)  # pin numbers: clk, dt, sw
rotary.add_handler(rotary_event)
val = 0

# I2C OLED setup
SCL_PIN = const(5)
SDA_PIN = const(4)
WIDTH  = 128                                          
HEIGHT = 32  
oled = display.disp_setup(SCL_PIN, SDA_PIN, WIDTH, HEIGHT)

# display initial reading
display.disp_string(oled, 5, 5, ('%d' %(val)))
print(val)

# loop
while True:
    time.sleep_ms(10)
