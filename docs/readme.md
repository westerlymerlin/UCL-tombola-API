# Module Documentation


This document contains the documentation for all the modules in the **Tombola-Py** version 1.7.5 application.

---

## Contents


[app](./app.md)  
This is the main flask application - called by Gunicorn
Author: Gary Twinn

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.
Author: Gary Twinn

[logmanager](./logmanager.md)  
logmanager, setus up application logging. Ese the **logger** property to
write to the log.
Author: Gary Twinn

[motor_class](./motor_class.md)  
motor_class module, provides the control to the v20 controller and reads from the rpm module
Author: Gary Twinn

[rpm_class](./rpm_class.md)  
rpm_class module, reads pulses from abs sensor and convert to RPM
Author: Gary Twinn

[tom_cmd](./tom_cmd.md)  
A basic command line app to allow a user connected to the raspberry pi console via TTY or SSH
to send stop start messages to the app.


---

