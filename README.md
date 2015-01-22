PyApex
======

Python3 Library for controlling Apex equipments
=======
Python3 Library for controlling Apex Technologies equipments


Installation
============

1. Clone the Git repository in your local machine, in the "Lib" directory of your Python 3.x distribution

Utilisation
===========

1. To access to the help and see all possibilities of PyApex, import the module :
	import PyApex
	help(PyApex)

2. In your Python 3.x script, import the PyApex module. For exemple, if you want to remote control an AP1000 equipment, import the AP1000 sub-module of PyApex as below
	import PyApex.AP1000 as AP1000

3. Connect to the equipment. For an AP1000, you can use
	RemoteEquipment = AP1000("XXX.XXX.XXX.XXX", Simulation=False)
where XXX.XXX.XXX.XXX is the IP address of the equipment
and Simulation argument is a boolean to simulate the equipment

4. To initiate a module of an AP1000 equipement, use the corresponding class and give the slot number in parameter. For exemple, to control an AP1000 power meter module (AP3314), you can use
	AP1000_Power_Meter = RemoteEquipment.PowerMeter(1)
where 1 is the slot number of the module

5. To close the connection to the equipment, use the Close function. For exemple
	RemoteEquipment.Close()

