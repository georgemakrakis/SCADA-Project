# SCADA-Project
A small SCADA network that receivess and sends information from/to remote devices from/to a control center. This project is part of the semester project for "University of Idaho, Supervisory Control and Critical Infrastructure Systems, Spring 2020" class.

## Arcitecture

1 PLC/RTU that receives information from a temperature sesnor and trasmits them via Modbus (and DNP3?) to a control center.

1 PLC/RTU that receives manual high/low level information of a tank and trasmits them via Modbus (and DNP3?) to a control center.

1 HMI that displays all the necessary information to the operators in the control center.

![alt text](https://github.com/georgemakrakis/SCADA-Project/blob/master/images/SCADA_Project_Architecture.png?raw=true)

## Equipment

The equipment fot hsi project is fffairly simple. It comrise of two 
Raspberry Pi that will play the role of a PLC, a router used to create a 
local network, and a laptop that will host the HMI.

![alt text](https://github.com/georgemakrakis/SCADA-Project/blob/master/images/Equipment.png?raw=true)

## Updates

DNP3 will not be used for now in the project, further investigation needed



