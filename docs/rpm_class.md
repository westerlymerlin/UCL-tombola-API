# Contents for: rpm_class

* [rpm\_class](#rpm_class)
  * [datetime](#rpm_class.datetime)
  * [GPIO](#rpm_class.GPIO)
  * [settings](#rpm_class.settings)
  * [logger](#rpm_class.logger)
  * [RPMClass](#rpm_class.RPMClass)
    * [\_\_init\_\_](#rpm_class.RPMClass.__init__)
    * [\_\_del\_\_](#rpm_class.RPMClass.__del__)
    * [recievedpulse](#rpm_class.RPMClass.recievedpulse)
    * [get\_rpm](#rpm_class.RPMClass.get_rpm)
    * [get\_rpm\_data](#rpm_class.RPMClass.get_rpm_data)

<a id="rpm_class"></a>

# rpm\_class

RPM Calculation Module

This module provides functionality to calculate vehicle wheel RPM (Revolutions Per Minute)
by processing pulses from an ABS (Anti-lock Braking System) sensor connected to a Raspberry Pi GPIO.

The module:
- Detects and timestamps ABS sensor pulses via GPIO input
- Calculates RPM based on rolling averages of pulse intervals
- Handles timeout detection for wheel stoppage
- Provides both RPM values and raw timing data

Requirements:
- Raspberry Pi with GPIO configured
- ABS sensor connected to the specified GPIO pin
- Configuration settings from app_control.settings

<a id="rpm_class.datetime"></a>

## datetime

<a id="rpm_class.GPIO"></a>

## GPIO

<a id="rpm_class.settings"></a>

## settings

<a id="rpm_class.logger"></a>

## logger

<a id="rpm_class.RPMClass"></a>

## RPMClass Objects

```python
class RPMClass()
```

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

<a id="rpm_class.RPMClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="rpm_class.RPMClass.__del__"></a>

#### \_\_del\_\_

```python
def __del__()
```

used when app is exiting to cleanup the GPIO settings

<a id="rpm_class.RPMClass.recievedpulse"></a>

#### recievedpulse

```python
def recievedpulse(pin)
```

runs when the abs sensor activates the gpio pin

<a id="rpm_class.RPMClass.get_rpm"></a>

#### get\_rpm

```python
def get_rpm()
```

calculate and return the rpm

<a id="rpm_class.RPMClass.get_rpm_data"></a>

#### get\_rpm\_data

```python
def get_rpm_data()
```

return the time intervals between the abs pulses for one revolution

