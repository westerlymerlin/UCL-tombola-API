import datetime
from time import sleep
from RPi import GPIO


class RPM:
    def __init__(self, magnets, gpio_line):
        self.magnets = magnets  # no of magnets on the wheel per revolution
        self.rev_average = 3  # rolling average over 3 revolutions
        self.gpio_line = gpio_line # line used for sensing the hall effect device
        self.timequeuesize = self.magnets * self.rev_average
        self.timequeue = []
        GPIO.setup(self.gpio_line, GPIO.IN)
        GPIO.add_event_detect(self.gpio_line, GPIO.RISING, callback=self.recievedpulse(), bouncetime=200)

    def recievedpulse(self):
        self.timequeue.append(datetime.datetime.now())
        if len(self.timequeue) > self.timequeuesize:
            self.timequeue.pop(0)

    def get_rpm(self):
        if len(self.timequeue) == self.timequeuesize:
            print("calculate RPM")
            rev = 60 / ((self.timequeue[self.timequeuesize - 1] - self.timequeue[0]).total_seconds() / self.rev_average)
            print('%s RPM' % rev)
            return rev
        else:
            print('Not enough pulses recieved yet')
            return 0


if __name__ == '__main__':
    rpm = RPM(3, 26)
    print('loading some test data')
    for i in range(30):
        rpm.recievedpulse()
        sleep(0.2)
    print('ready to test')
    rpm.get_rpm()
