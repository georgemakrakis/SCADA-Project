# SCADA-Project
A small SCADA network that recevies and send information to remote devices from a control center. This project is part of the semester project for University of Idaho Supervisory Control and Critical Infrastructure Systems, Spring 2020 class.

## Arcitecture

1 PLC/RTU that receives information from a temperature sesnor and trasmits them via Modbus and DNP3 to a control center.

1 PLC/RTU that receives manual open/close input heater information trasmits them Modbus and DNP3 to a control center.

1 HMI that displays all the necessary information to the operators in the control center.



