
PyApex
======

Python3 Library for controlling Apex equipments

***
**Installation**<br><br>
1. Download the package PyApex<br><br>
2. Unzip it and move it in the "Lib" directory of your Python 3.x distribution
***
**Using**<br><br>
1. To access to the help and see all possibilities of PyApex, import the module :<br> 
`import PyApex`<br>
`help(PyApex)`<br>
With PyApex, you can communicate with AP1000 (Ethernet), AP2XXX (Ethernet), AB3510 (USB) and XU Thermal Etuve (RS232).<br><br>
**AP1000**<br><br>
The AP1000 class allows you to control (via Ethernet) any AP1000 equipment (AP1000-2, AP1000-5 and AP1000-8)<br><br>
1. In your Python 3.x script, import the PyApex module. For exemple, if you want to remote control an AP1000 equipment, import the AP1000 sub-module of PyApex as below<br>
`import PyApex.AP1000 as AP1000`<br><br>
2. Connect to the equipment. For an AP1000, you can use<br>
`MyAP1000 = AP1000("192.168.0.10", Simulation=False)`<br>
where `192.168.0.10` is the IP address of the equipment<br>
and `Simulation` argument is a boolean to simulate the equipment<br><br>
3. To see the methods and attributs of the AP1000 class, do:<br>
`help(MyAP1000)`<br><br>
4. To initiate a module of an AP1000 equipement, use the corresponding class and give the slot number in parameter. For exemple, to control an AP1000 power meter module (AP3314), you can use<br>
`MyPowerMeter = MyAP1000.PowerMeter(1)`<br>
where `1` is the slot number of the module<br>
and for seeing the different methods and attributs associated to this module, do:<br>
`help(MyPowerMeter)`<br><br>
5. To close the connection to the equipment, use the Close function. For exemple<br>
`MyAP1000.Close()`<br><br>
**AP2XXX**<br><br>
The AP2XXX class allows you to control (via Ethernet) any OSA and OCSA equipment (AP2040, AP2050, AP2060, AP2443,...)<br><br>
1. In your Python 3.x script, import the PyApex module. For exemple, if you want to remote control an AP2040 equipment, import the AP2XXX sub-module of PyApex as below<br>
`import PyApex.AP2XXX as AP2040`<br><br>
2. Connect to the equipment:<br>
`MyOSA = AP2040("192.168.0.10", Simulation=False)`<br>
where `192.168.0.10` is the IP address of the equipment<br>
and `Simulation` argument is a boolean to simulate the equipment<br><br>
3. To see the methods and attributs of the AP2XXX class, do:<br>
`help(MyOSA)`<br><br>
4. To close the connection to the equipment, use the Close function:<br>
`MyOSA.Close()`<br><br>
