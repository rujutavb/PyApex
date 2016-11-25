'''
Python 3 package for controlling Apex Technologies equipments

    PyApex.AP1000 allows to control an AP1000 mainframe via Ethernet protocol
    "help(PyApex.AP1000)" for more details

    PyApex.AP2XXX allows to control an AP2XXX OSA and OCSA via Ethernet protocol
    "help(PyApex.AP2XXX)" for more details

    PyApex.AB3510 allows to control a board AB3510 quad photodetectors via USB 2.0 protocol
    this class requires PyUSB module installed
    "help(PyApex.AB3510)" for more details

    PyApex.AB3380 allows to control a board AB3380 dual filters via USB 2.0 protocol
    this class requires PyUSB module installed
    "help(PyApex.AB3380)" for more details

    PyApex.Etuve allows to control a XU Thermal Etuve via RS232 protocol
    this class requires PySerial module installed
    "help(PyApex.Etuve)" for more details
'''

from PyApex.AP1000 import AP1000
from PyApex.AP2XXX import AP2XXX
from PyApex.AB3510 import AB3510
from PyApex.AB3380 import AB3380
from PyApex.Etuve import Etuve

from PyApex.Constantes import Celerity


Version = 1.01
PythonVersion = 3.4

def version():
    return Version

def python():
    return PythonVersion
