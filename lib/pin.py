# from .basic import _Basic_class
#import RPi.GPIO as GPIO
from periphery import GPIO

class Pin(object):
    OUT = "out"
    IN = "out"
    IRQ_FALLING = "FALLING"
    IRQ_RISING = "RISING"
    IRQ_RISING_FALLING = "BOTH"
    PULL_UP = "pull_up"
    PULL_DOWN = "pull_down"
    PULL_NONE = None

    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    _dict_2 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25, # Changed
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5, # Changed
    }
    _dict_3 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  0, #chip 0
        "D3":  2, #chip 2
        "D4":  2, #chip 2
        "D5":  0, #chip 0
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25, # Changed
        "LED": 2, #chip 2
        "BOARD_TYPE": 0, # chip 0
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  0, # chip0
    }
    _line_1 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  6, # line 6
        "D3":  0, # PIN15, line 0
        "D4":  9, #PIN16, line 9
        "D5":  7, # line 7
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25, # Changed
        "LED": 13, #line 13
        "BOARD_TYPE": 0, #line 0
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  7, # line 7
    }

    def __init__(self, *value):
        super().__init__()
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)

        self.check_board_type()

        if len(value) > 0:
            pin = value[0]
        if len(value) > 1:
            mode = value[1]
        else:
            mode = None
        if len(value) > 2:
            setup = value[2]
        else:
            setup = None
        if isinstance(pin, str):
            try:
                self._board_name = pin
                self._pin = self.dict()[pin]
                self._line = self.line_list()[pin]
                print(self._line)
            except Exception as e:
                print(e)
                self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        elif isinstance(pin, int):
            print("no line number set")
            self._pin = pin
        else:
            self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        self._value = 0
        self.init(mode, pull=setup)
        # self._info("Pin init finished.")

    def check_board_type(self):
        type_pin = self.dict()["BOARD_TYPE"]
        self._dict = self._dict_3
        self._line_list = self._line_1
        # GPIO.setup(type_pin, GPIO.IN)
        # if GPIO.input(type_pin) == 0:
        #     self._dict = self._dict_1
        # else:
        #     self._dict = self._dict_2

    def init(self, mode, pull=PULL_NONE):
        self._pull = pull
        self._mode = mode
        if mode != None: ##TODO
            if pull != None:
                self.gpio1 = GPIO("/dev/gpiochip"+str(self._pin),int(self._line), mode)
                #GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                self.gpio1 = GPIO( "/dev/gpiochip"+str(self._pin),int(self._line),mode)
        else:
            self.gpio1 = GPIO("/dev/gpiochip"+str(self._pin),int(self._line),"in")
    def line_list(self, *_line_list):
        if len(_line_list) == 0:
            return self._line_list
        else:
            if isinstance(_line_list, dict):
                self._dict = _line_list
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _line_list)

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict)

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            self.mode(self.IN)
            result = self.gpio1.read(s)
            #result = GPIO.input(self._pin)
            # self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:
            value = value[0]
            self.mode(self.OUT)
            self.gpio1.write(value)
            #GPIO.output(self._pin, value)
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return self._mode
        else:
            mode = value[0]
            self._mode = mode
            self.gpio1.direction = mode

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)
        # GPIO.add_event_detect(self._pin, trigger, callback=handler, bouncetime=bouncetime)

    def name(self):
        return "GPIO%s"%self._pin

    def names(self):
        return [self.name, self._board_name]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4  = 4
        GPIO5  = 5
        GPIO6  = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass


if __name__ == "__main__":
    import time
    mcu_reset = Pin("MCURST")
    mcu_reset.off()
    time.sleep(0.001)
    mcu_reset.on()
    time.sleep(0.01)
