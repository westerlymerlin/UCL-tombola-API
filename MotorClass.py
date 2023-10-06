import minimalmodbus
from settings import settings


class Motor:
    def __init__(self):
        self.message_start = settings['reading_offset'] - 40001
        self.controller = minimalmodbus.Instrument(settings['port'], settings['station'], minimalmodbus.MODE_RTU)
        self.controller.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.controller.serial.baudrate = settings['baud']
        self.controller.serial.bytesize = settings['bytesize']
        self.controller.serial.stopbits = settings['stopbits']
        self.controller.serial.timeout = settings['timeout']
        self.controller.clear_buffers_before_each_transaction = settings['clear_buffers_before_call']
        self.controller.close_port_after_each_call = settings['clear_buffers_after_call']
        self.read_length = settings['read_length']
        self.direction = 0  # 0 = stop, 1 = forward, 2 = reverse
        self.frequency = 0  # 0 - 50 Hz

    def forward(self, speed):
        self.direction = 1
        self.frequency = speed
        self.controller_command([self.frequency, self.direction])

    def reverse(self, speed):
        self.direction = 2
        self.frequency = speed
        self.controller_command([self.frequency, self.direction])

    def stop(self):
        self.direction = 0
        self.frequency = 0
        self.controller_command([self.frequency, self.direction])

    def controller_command(self, message):
        self.controller.write_registers(self.message_start, message)
        self.controller.serial.close()

    def controller_query(self):
        data = self.controller.read_registers(self.message_start, self.read_length, 3)
        self.controller.serial.close()
        returnvalue ={}
        returnvalue['output-current'] = data[0]/10
        returnvalue['frequency'] = data[1]/100
        returnvalue['output-voltage'] = data[2]
        returnvalue['bus-voltage'] = data[3]
        returnvalue['power'] = data[4]/10
        returnvalue['operation'] = data[5]
        return returnvalue

tombola_motor = Motor()
