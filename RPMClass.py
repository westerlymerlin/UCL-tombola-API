import datetime
from RPi import GPIO
from settings import settings


class RPM:
    def __init__(self):
        self.magnets = settings['rpm_magnets']  # no of magnets on the wheel per revolution
        self.rev_average = 3  # rolling average revolutions
        self.gpio_line = settings['rpm_sensor_GPIO']  # line used for sensing the hall effect device
        self.rpm_timeout = settings['rpm_timeout_seconds']
        self.timequeuesize = self.magnets * self.rev_average
        self.timequeue = []
        GPIO.setmode(GPIO.BCM)  # set the GPIO to use Broadcom channel numbering
        GPIO.setup(self.gpio_line, GPIO.IN)  # set the input sensor
        GPIO.add_event_detect(self.gpio_line, GPIO.RISING, callback=self.recievedpulse, bouncetime=10)
        GPIO.setup(settings['rpm_active_LED'], GPIO.OUT)  # set running LED channel
        GPIO.output(settings['rpm_active_LED'], GPIO.HIGH)  # switch on running LED

    def __del__(self):
        print("RPM deleted")
        GPIO.cleanup()

    def recievedpulse(self, pin):
        self.timequeue.append(datetime.datetime.now())
        # print(self.timequeue)
        if len(self.timequeue) > self.timequeuesize:
            self.timequeue.pop(0)

    def get_rpm(self):
        if len(self.timequeue) == self.timequeuesize:
            rev = 60 / ((self.timequeue[self.timequeuesize - 1] - self.timequeue[0]).total_seconds() / self.rev_average)
            # print('%s RPM' % rev)
            if (datetime.datetime.now() - self.timequeue[self.timequeuesize - 1]).total_seconds() > self.rpm_timeout:
                self.timequeue.pop(0)
            return rev
        else:
            print('Not enough RPM pulses recieved, checl +12v is connected')
            return 0


if __name__ == '__main__':  # used for standlone testing
    rpm = RPM()
    x = True
    while x:
        x = input('any key to continue')
        print('RPM=%s' % rpm.get_rpm())
    GPIO.cleanup()
