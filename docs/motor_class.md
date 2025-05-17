# Contents for: motor_class

* [motor\_class](#motor_class)
  * [sleep](#motor_class.sleep)
  * [Timer](#motor_class.Timer)
  * [datetime](#motor_class.datetime)
  * [minimalmodbus](#motor_class.minimalmodbus)
  * [serialutil](#motor_class.serialutil)
  * [settings](#motor_class.settings)
  * [writesettings](#motor_class.writesettings)
  * [RPMClass](#motor_class.RPMClass)
  * [logger](#motor_class.logger)
  * [MotorClass](#motor_class.MotorClass)
    * [\_\_init\_\_](#motor_class.MotorClass.__init__)
    * [set\_speed](#motor_class.MotorClass.set_speed)
    * [rpm\_controller](#motor_class.MotorClass.rpm_controller)
    * [stop](#motor_class.MotorClass.stop)
    * [controller\_command](#motor_class.MotorClass.controller_command)
    * [controller\_query](#motor_class.MotorClass.controller_query)
    * [print\_controlword](#motor_class.MotorClass.print_controlword)
    * [read\_register](#motor_class.MotorClass.read_register)
    * [write\_register](#motor_class.MotorClass.write_register)
    * [set\_stop\_time](#motor_class.MotorClass.set_stop_time)
    * [get\_stop\_time](#motor_class.MotorClass.get_stop_time)
    * [auto\_stop\_timer](#motor_class.MotorClass.auto_stop_timer)
    * [parse\_control\_message](#motor_class.MotorClass.parse_control_message)
  * [running](#motor_class.running)
  * [time\_format\_check](#motor_class.time_format_check)

<a id="motor_class"></a>

# motor\_class

Motor Control Module for V20 Controller

This module provides a comprehensive interface for controlling an electric motor via a V20 controller
using Modbus RTU protocol over RS485. It handles motor speed control, direction, auto-shutdown,
and monitoring of motor parameters including RPM, voltage, and current.

Key features:
- Two-way communication with V20 motor controller via Modbus RTU
- Real-time RPM monitoring and speed adjustment
- Auto-shutdown capability based on configurable timer
- Error handling for connection issues and timeouts
- Comprehensive logging of motor operations and errors

Dependencies:
- minimalmodbus: Handles Modbus RTU communication
- serial: Manages serial port connections
- rpm_class: Provides actual motor speed measurement
- app_control: Manages application settings
- logmanager: Handles logging

<a id="motor_class.sleep"></a>

## sleep

<a id="motor_class.Timer"></a>

## Timer

<a id="motor_class.datetime"></a>

## datetime

<a id="motor_class.minimalmodbus"></a>

## minimalmodbus

<a id="motor_class.serialutil"></a>

## serialutil

<a id="motor_class.settings"></a>

## settings

<a id="motor_class.writesettings"></a>

## writesettings

<a id="motor_class.RPMClass"></a>

## RPMClass

<a id="motor_class.logger"></a>

## logger

<a id="motor_class.MotorClass"></a>

## MotorClass Objects

```python
class MotorClass()
```

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

<a id="motor_class.MotorClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="motor_class.MotorClass.set_speed"></a>

#### set\_speed

```python
def set_speed(required_rpm)
```

Sets the motor speed to the specified revolutions per minute (RPM). Validates
the input, ensuring it is converted to a valid number, within allowable limits,
and adjusts the operation of the motor accordingly.

Args:
    required_rpm (float): The desired speed in revolutions per minute (RPM).
        Must be a positive number and should not exceed the preconfigured
        maximum RPM value.

Returns:
    None

<a id="motor_class.MotorClass.rpm_controller"></a>

#### rpm\_controller

```python
def rpm_controller()
```

takes the speed in rpm and the desired speed and sets the controller frequency
if the speed varies it will bump the frequency by +- the frequiency_rpm value to
keep rpm withjin 0.1 rpm. Multi threadedd with threads running every 10 seconds
when the machine is running

<a id="motor_class.MotorClass.stop"></a>

#### stop

```python
def stop()
```

Stops the motor operation by resetting operational parameters and sending
the stop command to the controller. Handles exceptions for communication
issues with the motor controller.

Raises:
    AttributeError: If the RS485 Controller is absent or incorrectly
    initialized, triggering an error.
    minimalmodbus.NoResponseError: If the RS485 communication times out,
    signaling a communication error.

<a id="motor_class.MotorClass.controller_command"></a>

#### controller\_command

```python
def controller_command(message)
```

Sends the message (a number of words) to the v20 starting at the
command_start_register

<a id="motor_class.MotorClass.controller_query"></a>

#### controller\_query

```python
def controller_query()
```

Reads from the controller, starting at the query_start_register and
returns the read_length number of consecutive registers

<a id="motor_class.MotorClass.print_controlword"></a>

#### print\_controlword

```python
def print_controlword()
```

Writes the value of the STW control word to the application log (used for debugging)

<a id="motor_class.MotorClass.read_register"></a>

#### read\_register

```python
def read_register(reg)
```

returns the value of the registry specified via the API

<a id="motor_class.MotorClass.write_register"></a>

#### write\_register

```python
def write_register(reg, controlword)
```

api call that writes the controlword specified into the v20 register specified

<a id="motor_class.MotorClass.set_stop_time"></a>

#### set\_stop\_time

```python
def set_stop_time(autostop, stoptime)
```

website call or API call that sets the stop timer consists of a boolean switch 'autostop'
and at time HH:MM:SS

<a id="motor_class.MotorClass.get_stop_time"></a>

#### get\_stop\_time

```python
def get_stop_time()
```

Returns the stop time and is the autostop function is enabled

<a id="motor_class.MotorClass.auto_stop_timer"></a>

#### auto\_stop\_timer

```python
def auto_stop_timer()
```

Thread that checks if the time has matched the autostop time and stops the motor

<a id="motor_class.MotorClass.parse_control_message"></a>

#### parse\_control\_message

```python
def parse_control_message(message)
```

Processes the control messages for motor operations by interpreting the keys in the provided message
dictionary and performing corresponding actions, such as stopping the motor, setting the RPM, resetting
the controller, accessing registers, or updating stop time. Returns responses for specific queries.

Args:
    message (dict): A dictionary containing control instructions, where keys indicate the type
    of action to perform (e.g., 'stop', 'websetrpm') and values provide additional details
    for those actions.

Raises:
    None

Returns:
    Optional[dict]: Response data for specific queries such as reading registers or fetching
    RPM data. If no response is applicable, returns the result of `controller_query()`.

<a id="motor_class.running"></a>

#### running

```python
def running(value)
```

Returns text value based on running state

<a id="motor_class.time_format_check"></a>

#### time\_format\_check

```python
def time_format_check(value)
```

Tests if a time string is in the correct format

