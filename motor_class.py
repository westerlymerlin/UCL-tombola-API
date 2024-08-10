"""
motor_class module, provides the control to the v20 controller and reads from the rpm module
Author: Gary Twinn
"""

from threading import Timer
from datetime import datetime
import minimalmodbus
import serial.serialutil
from app_control import settings, writesettings
from rpm_class import RPMClass
from logmanager import logger


class MotorClass:
    """
    Represents a motor controller.

    Attributes:
        command_start_register (int): Starting register for sending commands.
        stw_control_register (int): Control register for the STW.
        query_start_register (int): Starting register for querying the controller.
        controller (Instrument): MinimalModbus instrument for communicating with the controller.
        read_length (int): Number of consecutive registers to read.
        direction (int): Direction of motor rotation (0 - forward, 1 - reverse).
        frequency (float): Motor frequency (0-100%).
        running (int): Status of motor (0 - disabled, 1 - enabled).
        autoshutdown (bool): Flag indicating whether autoshutdown is enabled.
        autoshutdowntime (int): Time after which the motor is shutdown if not used (in minutes).
        rpm_hz (float): Conversion factor from RPM to Hz.
        requested_rpm (float): Requested motor speed in RPM.
        rpm (RPMClass): RPMClass object for getting actual motor speed.
    """
    def __init__(self):
        self.command_start_register = settings['control_start_register']
        self.stw_control_register = settings['STW_register']
        self.query_start_register = settings['reading_start_register']
        self.read_length = settings['read_length']
        self.direction = 0  # 0 = forward, 1 = reverse
        self.frequency = 0  # 0 - 100%
        self.running = 0  # O = disabled 1 = enabled
        self.autoshutdown = settings['autoshutdown']
        self.autoshutdowntime = settings['shutdowntime']
        self.rpm_hz = settings['rpm_frequency']
        self.requested_rpm = 0
        self.serialaccess = False
        self.rpm = RPMClass()
        self.auto_stop_timer()
        try:
            self.controller = minimalmodbus.Instrument(settings['port'], settings['station'],
                                                       minimalmodbus.MODE_RTU)
            self.controller.serial.parity = minimalmodbus.serial.PARITY_EVEN
            self.controller.serial.baudrate = settings['baud']
            self.controller.serial.bytesize = settings['bytesize']
            self.controller.serial.stopbits = settings['stopbits']
            self.controller.serial.timeout = settings['serialtimeout']
            self.controller.clear_buffers_before_each_transaction = \
                settings['clear_buffers_before_call']
            self.controller.close_port_after_each_call = settings['clear_buffers_after_call']
            logger.debug('MotorClass: RS485 controller setup with modbus')
            # logger.debug('MotorClass: Resetting v20')
            # self.write_register(self.stw_control_register, settings['STW_forward'])
            # logger.debug('MotorClass: settimg speed to 0')
            # self.stop()
        except serial.serialutil.SerialException:
            logger.error('MotorClass: init Error - no controller connected, '
                         'please check RS485 port address is correct')

    def set_speed(self, required_rpm):
        """called by the api or web page to change the desired speed"""
        try:
            required_rpm = int(float(required_rpm) * 10)/10
        except ValueError:
            return
        if required_rpm < 0.1:
            self.stop()
            return
        required_rpm = min(required_rpm, settings['rpm_max'])
        self.running = 1
        self.direction = 0
        self.requested_rpm = required_rpm
        self.rpm_controller()
        logger.debug('MotorClass: Set speed: %s', required_rpm)

    def rpm_controller(self):
        """takes the speed in rpm and the desired speed and sets the controller frequency
           if the speed varies it will bump the frequency by +- the frequiency_rpm value to
           keep rpm withjin 0.1 rpm. Multi threadedd with threads running every 10 seconds
           when the machine is running"""
        rpm = self.rpm.get_rpm()
        speedchanged = 1
        if self.running:  # run this check in 10s if the drum is running
            rpmthread = Timer(10, self.rpm_controller)
            rpmthread.name = 'RPM Reader Thread'
            rpmthread.start()
        else:
            return
        speed_diff = rpm - self.requested_rpm  # Difference between actual and requested rpm
        if abs(speed_diff) > 5:
            logger.debug('MotorClass: RPM diff > 5 so reseting')
            self.frequency = int(10 * self.requested_rpm * self.rpm_hz)
        elif speed_diff > 0.1:
            logger.debug('MotorClass: RPM slightly to high, reducing it a bit')
            self.frequency = int(self.frequency - self.rpm_hz)
        elif speed_diff < -0.1:
            logger.debug('MotorClass: RPM slightly to low, increasing it a bit')
            self.frequency = int(self.frequency + self.rpm_hz)
        else:
            speedchanged = 0
            rpm_hz = (self.frequency / self.rpm.get_rpm()) / 10  # calculate the steady rpm-hz ratio
            if abs(rpm_hz - self.rpm_hz) > 5:
                logger.info('MotorClass: rpm_hz value should be = %s', rpm_hz)
        if speedchanged:
            try:
                logger.info('Motorclass: RPM Controller: Current RPM %.2f Desired %.2f setting to frequency %s',
                            rpm, self.requested_rpm, self.frequency)
                self.controller_command([self.frequency, self.running, self.direction, 1])
            except AttributeError:
                logger.error('MotorClass: rpm_controller function error No RS483 Controller')
                self.serialaccess = False
            except minimalmodbus.NoResponseError:
                logger.error('MotorClass: rpm_controller function error RS485 timeout')
                self.serialaccess = False


    def stop(self):
        """Called by the API or web page to stop the motor"""
        self.direction = 0
        self.frequency = 0
        self.requested_rpm = 0
        self.running = 0
        try:
            logger.info('MotorClass: STOP requested')
            self.controller_command([self.frequency, self.running, self.direction, 0])
            self.serialaccess = False
        except AttributeError:
            self.serialaccess = False
            logger.error('MotorClass: Stop function error No RS483 Controller')
            self.serialaccess = False
        except minimalmodbus.NoResponseError:
            self.serialaccess = False
            logger.error('MotorClass: Stop function error RS485 timeout')


    def controller_command(self, message):
        """Sends the message (a number of words) to the v20 starting at the
        command_start_register"""
        while self.serialaccess:
            pass
        self.controller.write_registers(self.command_start_register, message)
        self.controller.serial.close()
        self.serialaccess = False

    def controller_query(self):
        """Reads from the controller, starting at the query_start_register and
         returns the read_length number of consecutive registers """
        while self.serialaccess:
            pass
        self.serialaccess = True
        try:
            actual_data = self.controller.read_registers(self.query_start_register,
                                                         self.read_length, 3)
            setting_data = self.controller.read_registers(self.command_start_register, 4, 3)
            self.controller.serial.close()
            self.serialaccess = False
            return {'running': running(self.running), 'reqfrequency': setting_data[0] / 100,
                    'frequency': actual_data[0] / 100, 'voltage': actual_data[9], 'current':
                        actual_data[2] / 100,
                    'rpm': actual_data[1], 'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except AttributeError:   # RS485 not plugged in
            self.controller.serial.close()
            self.serialaccess = False
            logger.error('MotorClass: Controller Query Error: RS485 controller is not '
                         'working or not plugged in')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': 'No RS485 Controller', 'voltage': 'No RS485 Controller',
                    'current': 'No RS485 Controller', 'rpm': 'No RS485 Controller',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except minimalmodbus.NoResponseError:
            self.controller.serial.close()
            self.serialaccess = False
            logger.error('MotorClass: Controller Query Error: No response from the V20 controller, '
                         'check it is powered on and connected')
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': 'RS485 Timeout', 'voltage': 'RS485 Timeout',
                    'current': 'RS485 Timeout', 'rpm': 'RS485 Timeout',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}
        except serial.serialutil.SerialException:
            self.controller.serial.close()
            self.serialaccess = False
            logger.error('MotorClass: Controller Query Error: unhandled ex eption', exc_info=BaseException)
            return {'running': running(self.running), 'reqfrequency': self.frequency / 100,
                    'frequency': '-', 'voltage': '-', 'current': '-', 'rpm': '-',
                    'tombola_speed': '%.2f' % self.rpm.get_rpm(),
                    'requested_speed': self.requested_rpm}

    def print_controlword(self):
        """Writes the value of the STW control word to the application log (used for debugging)"""
        data = self.controller.read_register(99, 0, 3)
        self.controller.serial.close()
        logger.info('Motorclass: read control word: %s', data)

    def read_register(self, reg):
        """returns the value of the registry specified via the API"""
        try:
            data = self.controller.read_register(reg, 0, 3)
            self.controller.serial.close()
            logger.debug('MotorClass: read registry: Registry %s. Word %s', reg, data)
            return {'register': reg, 'word': data}
        except AttributeError:
            logger.error('MotorClass: read_register function error No RS483 Controller')
            return {'register': reg, 'word': 'No RS485 Controller'}
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: read_register function error RS485 timeout')
            return {'register': reg, 'word': 'RS485 Timeout'}

    def write_register(self, reg, controlword):
        """api call that writes the controlword specified into the v20 register specified"""
        try:
            self.controller.write_register(reg, controlword)
            self.controller.serial.close()
            logger.info('MotorClass: write registry: Registry %s. Word %s', reg, controlword)
        except AttributeError:
            logger.error('MotorClass: write_register function error No RS483 Controller')
        except minimalmodbus.NoResponseError:
            logger.error('MotorClass: write_register function error RS485 timeout')

    def set_stop_time(self, autostop, stoptime):
        """website call or API call that sets the stop timer consists of a boolean switch 'autostop'
        and at time HH:MM:SS"""
        if time_format_check(stoptime):
            self.autoshutdown = autostop
            settings['autoshutdown'] = autostop
            self.autoshutdowntime = stoptime
            settings['shutdowntime'] = stoptime
            logger.info('MotorClass: Write settings.json')
            writesettings()

    def get_stop_time(self):
        """Returns the stop time and is the autostop function is enabled"""
        return {'autostop': self.autoshutdown, 'stoptime': self.autoshutdowntime}

    def auto_stop_timer(self):
        """Thread that checks if the time has matched the autostop time and stops the motor"""
        timerthread = Timer(1, self.auto_stop_timer)
        timerthread.name = 'Auto Stop Thread'
        timerthread.start()
        if self.autoshutdown and self.running:
            stoptime = datetime.strptime(datetime.now().strftime('%d/%m/%Y ') +
                                         self.autoshutdowntime, '%d/%m/%Y %H:%M:%S')
            # print(stoptime)
            if stoptime < datetime.now():
                logger.info('MotorClass: Auto stop time reached - stopping')
                self.stop()

    def parse_control_message(self, message):
        """Parser that recieves messages from the API or web page posts and directs
        messages to the correct function"""
        if 'stop' in message.keys():
            logger.debug('MotorClass: Stop request recieved from web application')
            self.stop()
        elif 'websetrpm' in message.keys():
            logger.debug('MotorClass: RPM set by web application')
            self.set_speed(message['websetrpm'])
        elif 'setrpm' in message.keys():
            logger.debug('MotorClass: RPM set by API')
            self.set_speed(message['setrpm'])
        elif 'reset' in message.keys():
            logger.debug('MotorClass: Controller reset requested by web application')
            self.write_register(self.stw_control_register, settings['STW_forward'])
        elif 'write_register' in message.keys():
            logger.debug('MotorClass: Write Register recieved via API')
            self.write_register(message['write_register'], message['word'])
        elif 'read_register' in message.keys():
            logger.debug('MotorClass: Read Register recieved via API')
            return self.read_register(message['read_register'])
        elif 'rpm_data' in message.keys():
            logger.debug('MotorClass: RPM timing data request via API')
            return self.rpm.get_rpm_data()
        elif 'rpm' in message.keys():
            logger.debug('MotorClass: RPM speed request via API')
            return {'rpm': self.rpm.get_rpm()}
        elif 'stoptime' in message.keys():
            if 'autostop' in message.keys():
                self.set_stop_time(True, message['stoptime'])
            else:
                self.set_stop_time(False, message['stoptime'])
            logger.debug('Stop time updated via web application')
        else:
            logger.info('MotorClass: API message recieved but not processed  = %s', message)
        return self.controller_query()


def running(value):
    """Returns text value based on running state"""
    if value == 1:
        return 'Running'
    return 'Stopped'


def time_format_check(value):
    """Tests if a time string is in the correct format"""
    try:
        datetime.strptime(value, '%H:%M:%S')
        return True
    except ValueError:
        return False


if __name__ == '__main__':  # used for standlone testing
    tom = MotorClass()
