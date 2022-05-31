'''
A class to read a KY-040 rotary encoder using interrupts.

Resources:
https://github.com/gurgleapps/rotary-encoder
https://gurgleapps.com/learn/electronics/ky-040-rotary-encoder-on-a-raspberry-pi-pico-detailed-explanation-and-step-by-step-code
'''

import machine
import utime as time
from machine import Pin
import micropython

class Rotary:
    
    ROT_CW = 1
    ROT_CCW = 2
    SW_PRESS = 4
    SW_RELEASE = 8
    
    def __init__(self,clk,dt,sw):
        self.dt_pin = Pin(dt, Pin.IN)   # use pullup on encoder breakout board
        self.clk_pin = Pin(clk, Pin.IN) # use pullup on encoder breakout board
        self.sw_pin = Pin(sw, Pin.IN)   # use pullup on encoder breakout board
        self.last_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        self.dt_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.clk_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.sw_pin.irq(handler=self.switch_detect, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.handlers = []
        self.last_button_status = self.sw_pin.value()
        
    def rotary_change(self, pin):
        new_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        if new_status == self.last_status:
            return
        transition = (self.last_status << 2) | new_status
        if transition == 0b1101:
            #micropython.schedule(self.call_handlers, Rotary.ROT_CW)
            # micropython.schedule() causing RuntimeError: schedule queue full
            # see https://docs.micropython.org/en/latest/library/micropython.html?highlight=schedule
            self.call_handlers(Rotary.ROT_CW)
        elif transition == 0b1110:
            #micropython.schedule(self.call_handlers, Rotary.ROT_CCW)
            self.call_handlers(Rotary.ROT_CCW)
        self.last_status = new_status
        
    def switch_detect(self,pin):
        if self.last_button_status == self.sw_pin.value():
            return
        self.last_button_status = self.sw_pin.value()
        if self.sw_pin.value():
            #micropython.schedule(self.call_handlers, Rotary.SW_RELEASE)
            self.call_handlers(Rotary.SW_RELEASE)
        else:
            #micropython.schedule(self.call_handlers, Rotary.SW_PRESS)
            self.call_handlers(Rotary.SW_PRESS)
            
    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def call_handlers(self, type):
        for handler in self.handlers:
            handler(type)
    