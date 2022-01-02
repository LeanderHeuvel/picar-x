#!/usr/bin/env python3
from i2c import I2C

class ADC(I2C):
    ADDR=0x68                   # The address of the expansion board is 0x14

    def __init__(self, chn):    # Parameters, number of channels, 8 adc channels on the Raspberry Pi expansion board are:"A0, A1, A2, A3, A4, A5, A6, A7"
        super().__init__()
        if isinstance(chn, str):
            if chn.startswith("A"):     # Determine whether the parameter coming through the boundary starts with A, if it is, take the number after A
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:          # Determine whether the extracted number is within the range of 0~7
            self._error('Incorrect channel range')
        chn = 7 - chn
        self.chn = chn | 0x10           # Give slave address
        self.reg = 0x40 + self.chn
        # self.bus = smbus.SMBus(1)
        
    def read(self):                     # adc channel read number---write data once, read data twice (the read data range is 0~4095)
        # self._debug("Write 0x%02X to 0x%02X"%(self.chn, self.ADDR))
        # self.bus.write_byte(self.ADDR, self.chn)      # data input
        self.send([self.chn, 0, 0], self.ADDR)

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_h = self.bus.read_byte(self.ADDR)
        value_h = self.recv(1, self.ADDR)[0]            # Read data

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_l = self.bus.read_byte(self.ADDR)
        value_l = self.recv(1, self.ADDR)[0]            # Read data (read twice)

        value = (value_h << 8) + value_l
        # self._debug("Read value: %s"%value)
        return value

    def read_voltage(self):                             # Convert the read data into a voltage value (0~3.3V)
        return self.read*3.3/4095
        

def test():
    import time
    adc = ADC(0)
    while True:
        print(adc.read())
        time.sleep(1)

if __name__ == '__main__':
    test()