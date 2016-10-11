=======
PyApex
======

Python3 Library for controlling Apex equipments

***
**Installation**<br><br>
1. Download the package PyApex<br><br>
2. Unzip it and move it in the "Lib" directory of your Python 3.x distribution
***
**Utilisation**<br><br>
1. To access to the help and see all possibilities of PyApex, import the module :<br> 
`import PyApex`<br>
`help(PyApex)`<br><br>
2. In your Python 3.x script, import the PyApex module. For exemple, if you want to remote control an AP1000 equipment, import the AP1000 sub-module of PyApex as below<br>
`import PyApex.AP1000 as AP1000`<br><br>
3. Connect to the equipment. For an AP1000, you can use<br>
`RemoteEquipment = AP1000("XXX.XXX.XXX.XXX", Simulation=False)`<br>
where `XXX.XXX.XXX.XXX` is the IP address of the equipment<br>
and `Simulation` argument is a boolean to simulate the equipment<br><br>
4. To initiate a module of an AP1000 equipement, use the corresponding class and give the slot number in parameter. For exemple, to control an AP1000 power meter module (AP3314), you can use<br>
`AP1000_Power_Meter = RemoteEquipment.PowerMeter(1)`<br>
where `1` is the slot number of the module<br><br>
5. To close the connection to the equipment, use the Close function. For exemple<br>
`RemoteEquipment.Close()`<br><br>
