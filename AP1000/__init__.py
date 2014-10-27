#! /usr/bin/python3
# -*- coding: <utf-8> -*-

import socket
import os, sys, re

from PyApex.AP1000.PowerMeter import PowerMeter
from PyApex.AP1000.Attenuator import Attenuator
from PyApex.AP1000.TunableLaser import TunableLaser
from PyApex.AP1000.ErbiumAmplifier import ErbiumAmplifier
from PyApex.Constantes import *
from PyApex.Errors import ApexError

class AP1000():
    '''
    NAME
        PyApex
        
    FILE
        DIST_PYTHON/Lib/PyApex/__init__.py
    
    DESCRIPTION
        Elementary functions to communicate with Apex AP1000 equipment
        this version can communicate with :
            - AP335X (Tunable Laser Module)
            - AP331X (Power Meter Module)
            - AP336X (Attenuator Module)
            - AP337X (Amplifier Module)
    
    VERSION
        1.0
    
    FUNCTIONS
    '''

    def __init__(self, IPaddress, PortNumber=5900, Simulation=False):
        '''
        Constructor of AP1000 equipment.
        IPaddress is the IP address of the equipment. It's a string data
        PortNumber is by default 5900. It's an integer
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        self.IPAddress = IPaddress
        self.PortNumber = PortNumber
        self.Simulation = Simulation
        self.Open()
        

    def Open(self):
        self.Connexion = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.Connexion.settimeout(10)
        self.Connexion.setblocking(True)
        
        if self.Simulation:
            print("Connected successfully to the equipment")
        else:
            try:
                self.Connexion.connect((self.IPAddress, self.PortNumber))
                print("Connected successfully to the equipment")
            except:
                print("Cannot connect to the equipment")
                sys.exit()


    def Close(self):
        if not self.Simulation:
            try:
                self.Connexion.close()
            except:
                raise ApexError(AP1000_ERROR_COMMUNICATION, self.Connexion.getsockname()[0])
                sys.exit()


    def GetID(self):
        if self.Simulation:
            return SimuAP1000_ID
        else:
            self.Send("*IDN?\n")
            ID = self.Receive()
            return ID


    def Reset(self):
        if not self.Simulation:
            self.Send("*RST\n")


    def Send(self, Command):
        if not isinstance(Command, str):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Command")
            sys.exit()
        try:
            self.Connexion.send(Command.encode('utf-8'))
        except:
            raise ApexError(AP1000_ERROR_BADCOMMAND, Command)
            sys.exit()


    def Receive(self, ByteNumber=1024):
        if not isinstance(ByteNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ByteNumber")
            sys.exit()
        try:
            data = self.Connexion.recv(ByteNumber)
        except:
            raise ApexError(AP1000_ERROR_COMMUNICATION, self.Connexion.getsockname()[0])
            sys.exit()
        else:
            return data.decode('utf-8')

      
    def SlotUsed(self, SlotNumber):
        if not isinstance(SlotNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "SlotNumber")
            sys.exit()
        if SlotNumber < AP1000_SLOT_MIN or SlotNumber > AP1000_SLOT_MAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "SlotNumber")
            sys.exit()
        
        if self.Simulation:
            ID = SimuAP1000_SlotUsed
        else:
            Command = "SLT[" + str(SlotNumber).zfill(2) + "]:EMPTY?\n"
            self.Send(Command)
            ID = self.Receive(10)
            
        if ID[:-1] == "0":
            return False
        elif ID[:-1] == "1":
            return True


    def SlotID(self, SlotNumber, Force=False):
        if not isinstance(SlotNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "SlotNumber")
            sys.exit()
        if SlotNumber < AP1000_SLOT_MIN or SlotNumber > AP1000_SLOT_MAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "SlotNumber")
            sys.exit()
        
        if self.Simulation:
            ID = SimuAP1000_SlotID
        else:
            if Force == True:
                SlotUsed = True
            else:
                SlotUsed = self.SlotUsed(SlotNumber)
            if SlotUsed:
                Command = "SLT[" + str(SlotNumber).zfill(2) + "]:IDN?\n"
                Error = self.Send(Command)
                ID = self.Receive()
            else:
                return "Slot not used"
            
        return ID[:-1]


    def SlotSN(self, SlotNumber, Force=False):
        if not isinstance(SlotNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "SlotNumber")
            sys.exit()
        if SlotNumber < AP1000_SLOT_MIN or SlotNumber > AP1000_SLOT_MAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "SlotNumber")
            sys.exit()

        if self.Simulation:
            SN = SimuAP1000_SlotID
        else:
            SN = self.SlotID(SlotNumber, Force=True)

        try:
            SN = SN.lower().split("/")[2].split("-")
            SN = SN[len(SN) - 1]
            SN = int(re.findall("\d+", SN)[0])
            return int(SN)
        except:
            raise ApexError(AP1000_ERROR_SLOT_NOT_DEFINED, SlotNumber)
            sys.exit()
    

    def SlotType(self, SlotNumber):
        if not isinstance(SlotNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "SlotNumber")
            sys.exit()
        if SlotNumber < AP1000_SLOT_MIN or SlotNumber > AP1000_SLOT_MAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "SlotNumber")
            sys.exit()
        
        if self.Simulation:
            ID = SimuAP1000_SlotID
        else:
            if self.SlotUsed(SlotNumber):
                ID = self.SlotID(SlotNumber)
            else:
                return "Slot not used"
            
        try:
            ID = ID.lower().split("/")[1].split("-")[0]
            ID = int(re.findall("\d+", ID)[0])
            return Modules[ID]
        except:
            raise ApexError(AP1000_ERROR_SLOT_NOT_DEFINED, SlotNumber)
            sys.exit()


    def PowerMeter(self, SlotNumber, Force=False):
        if Force == True:
            return PowerMeter(self, SlotNumber, self.Simulation)
        if self.Simulation or self.SlotType(SlotNumber) == AP1000_PWM_NAME:
            return PowerMeter(self, SlotNumber, self.Simulation)
        else:
            raise ApexError(AP1000_ERROR_SLOT_NOT_GOOD_TYPE, SlotNumber)
            sys.exit()


    def Attenuator(self, SlotNumber, Force=False):
        if Force == True:
            return Attenuator(self, SlotNumber, self.Simulation)
        if self.Simulation or self.SlotType(SlotNumber) == AP1000_ATT_NAME:
            return Attenuator(self, SlotNumber, self.Simulation)
        else:
            raise ApexError(AP1000_ERROR_SLOT_NOT_GOOD_TYPE, SlotNumber)
            sys.exit()


    def TunableLaser(self, SlotNumber, Force=False):
        if Force == True:
            return TunableLaser(self, SlotNumber, self.Simulation)
        if self.Simulation or self.SlotType(SlotNumber) == AP1000_TLS_CBAND_NAME \
           or self.SlotType(SlotNumber) == AP1000_TLS_LBAND_NAME:
            return TunableLaser(self, SlotNumber, self.Simulation)
        else:
            raise ApexError(AP1000_ERROO_SLOT_NOT_GOOD_TYPE, SlotNumber)


    def ErbiumAmplifier(self, SlotNumber, Force=False):
        if Force == True:
            return ErbiumAmplifier(self, SlotNumber, self.Simulation)
        if self.Simulation or self.SlotType(SlotNumber) == AP1000_EFA_PREAMP_NAME \
           or self.SlotType(SlotNumber) == AP1000_EFA_BOOST_NAME \
           or self.SlotType(SlotNumber) == AP1000_EFA_INLINE_NAME:
            return ErbiumAmplifier(self, SlotNumber, self.Simulation)
        else:
            raise ApexError(AP1000_ERROO_SLOT_NOT_GOOD_TYPE, SlotNumber)

