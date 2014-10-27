import sys, re

from PyApex.Constantes import *
from PyApex.Errors import ApexError

from math import log10 as log

class ErbiumAmplifier():

    def __init__(self, Equipment, SlotNumber, Simulation=False):
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.SlotNumber = SlotNumber
        self.Type = self.GetType()
        self.Unit = "dBm"
        self.Wavelength = 1550
        self.Amplification = 0
        self.IPump = 0
        self.ValidUnits = ["dbm", "mw"]
        
       
    def __str__(self):
        return "Erbium Amplifier in slot " + str(self.SlotNumber)

        
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


    def GetType(self):
        if self.Simulation:
            ID = SimuEFA_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            self.Send(Command)
            ID = self.Receive()

        if re.findall(str(AP1000_EFA_PREAMP), ID.split("/")[1]) != []:
            return 0
        elif re.findall(str(AP1000_EFA_BOOST), ID.split("/")[1]) != []:
            return 1
        elif re.findall(str(AP1000_EFA_INLINE), ID.split("/")[1]) != []:
            return 2
        else:
            raise ApexError(AP1000_ERROR_SLOT_TYPE_NOT_DEFINED, self.SlotNumber)
            sys.exit()
            
    
    def ConvertForWriting(self, Power):
        if self.Unit.lower() == "dbm":
            return Power
        elif self.Unit.lower() == "mw":
            try:
                log(Power)
            except:
                raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Power")
                sys.exit()
            else:
                return -10 * log(Power/100)
        else:
            raise ApexError(AP1000_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
            sys.exit()


    def ConvertForReading(self, Power):
        if self.Unit.lower() == "mw":
            return 10**(Power / 10)
        elif self.Unit.lower() == "dbm":
            return Power
        else:
            raise ApexError(AP1000_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
            sys.exit()


    def GetInVoltage(self):
        if self.Simulation:
            InVoltage = SimuEFA_InVoltage
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:POWERINVALUE\n"
            self.Send(Command)
            InVoltage = self.Receive()

        return int(InVoltage[:-1])


    def GetOutVoltage(self):
        if self.Simulation:
            InVoltage = SimuEFA_OutVoltage
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:POWEROUTVALUE\n"
            self.Send(Command)
            InVoltage = self.Receive()

        return int(InVoltage[:-1])


    def SetIPump(self, IPump):
        if not isinstance(IPump, (float, int)):
            raise ApexError(AP1000_ERROR__ARGUMENT_TYPE, "IPump")
            sys.exit()
        if IPump > AP1000_EFA_IPMAX[self.Type] or IPump < 0:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "IPump")
            sys.exit()

        if not self.Simulation:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:PUMP" + ("%.1f" % IPump) + "\n"
            self.Send(Command)

        self.IPump = IPump
    
    
    def GetInPower(self):      
        if self.Simulation:
            Power = SimuEFA_InPower
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:INDB?\n"
            self.Send(Command)
            Power = self.Receive()
        
        return float(Power[:-1])


    def GetOutPower(self):      
        if self.Simulation:
            Power = SimuEFA_OutPower
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:OTDB?\n"
            self.Send(Command)
            Power = self.Receive()
        
        return float(Power[:-1])
    
    
    def SetUnit(self, Unit):
        if not isinstance(Unit, str):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Unit")
            sys.exit()
        
        if Unit.lower() in self.ValidUnits:
            self.Unit = Unit
    
    
    def GetUnit(self):
        return self.Unit
