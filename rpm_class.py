"""
rpm_class module, reads pulses from abs sensor and converst to RPM
"""

import datetime
from RPi import GPIO
from settings import settings
from logmanager import logger


class RPMClass:
    """
    RPMClass

    Class for calculating RPM (Revolutions Per Minute) based on the time intervals between ABS pulses.

    Parameters:
    - magnets (int): Number of magnets on the wheel per revolution.
    - rev_average (int): Rolling average number of revolutions.
    - gpio_line (int): GPIO line used for the hall effect device.
    - rpm_timeout (int): Timeout in seconds for determining if the wheel has stopped.
    - timequeue (list): List for storing the timestamps of received ABS pulses.

    Methods:
    - __init__(self): Constructor method to initialize the class object.
    - __del__(self): Destructor method to cleanup the GPIO settings when the app is exiting.
    - recievedpulse(self, pin): Method runs when the ABS sensor activates the GPIO pin.
    - get_rpm(self): Method to calculate and return the RPM.
    - get_rpm_data(self): Method to return the time intervals between the ABS pulses for one revolution.
    """
    def __init__(self):
        self.magnets = settings['rpm_magnets']  # no of magnets on the wheel per revolution
        self.rev_average = 3  # rolling average revolutions
        self.gpio_line = settings['rpm_sensor_GPIO']  # line used for the hall effect device
        self.rpm_timeout = settings['rpm_timeout_seconds']
        self.timequeuesize = self.magnets * self.rev_average
        self.timequeue = []
        GPIO.setmode(GPIO.BCM)  # set the GPIO to use Broadcom channel numbering
        GPIO.setup(self.gpio_line, GPIO.IN)  # set the input sensor
        GPIO.add_event_detect(self.gpio_line, GPIO.RISING,
                              callback=self.recievedpulse, bouncetime=10)
        GPIO.setup(settings['rpm_active_LED'], GPIO.OUT)  # set running LED channel
        GPIO.output(settings['rpm_active_LED'], GPIO.HIGH)  # switch on running LED

    def __del__(self):
        """used when app is exiting to cleanup the GPIO settings"""
        logger.info("RPM deleted")
        GPIO.cleanup()

    def recievedpulse(self, pin):   # pylint: disable=W0613
        """runs when the abs sensor activates the gpio pin"""
        self.timequeue.append(datetime.datetime.now())
        # print(self.timequeue)
        if len(self.timequeue) > self.timequeuesize:
            self.timequeue.pop(0)

    def get_rpm(self):
        """calculate and return the rpm"""
        if len(self.timequeue) == self.timequeuesize:
            rev = 60 / ((self.timequeue[self.timequeuesize - 1]
                         - self.timequeue[0]).total_seconds() / self.rev_average)
            # print('%s RPM' % rev)
            if (datetime.datetime.now() - self.timequeue[self.timequeuesize - 1]).total_seconds()\
                    > self.rpm_timeout:
                self.timequeue.pop(0)
            return rev
        return 0

    def get_rpm_data(self):
        """return the time intervals between the abs pulses for one revolution"""
        returntime = []
        for i in range(self.magnets + 1):
            returntime.append((self.timequeue[i] - self.timequeue[0]).total_seconds())
        return returntime


if __name__ == '__main__':  # used for standlone testing
    rpm = RPMClass()
    X = True
    while X:
        X = input('any key to continue')
        print(f'RPM={rpm.get_rpm()}')
    GPIO.cleanup()
