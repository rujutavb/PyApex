import sys, re

from PyApex.Constantes import *
from PyApex.Errors import ApexError

from math import log10 as log
import time

class TunableLaser():

    def __init__(self, Equipment, SlotNumber, Simulation=False):
        self.Connexion = Equipment.Connexion
        self.SlotNumber = SlotNumber
        self.Simulation = Simulation
        self.Type = self.GetType()
        self.Unit = "dBm"
        self.Wavelength = 1550
        self.Power = 0
        self.Status = "OFF"
        self.ValidUnits = ["dbm", "mw"]
        
       
    def __str__(self):
        return "Tunable Laser in slot " + str(self.SlotNumber)

        
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
            ID = SimuTLS_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            self.Send(Command)
            ID = self.Receive()

        if re.findall(str(AP1000_TLS_CBAND), ID.split("/")[1]) != []:
            return 0
        elif re.findall(str(AP1000_TLS_CLBAND), ID.split("/")[1]) != []:
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
    
    
    def SetPower(self, Power):
        if not isinstance(Power, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Power")
            sys.exit()
            
        Power = self.ConvertForWriting(Power)
        if Power < AP1000_TLS_POWMIN[self.Type] or Power > AP1000_TLS_POWMAX[self.Type]:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Power")
            sys.exit()
            
        if self.Simulation:
            self.Power = Power
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TPDB" + ("%.1f" % Power) + "\n"
            self.Send(Command)
            self.Power = Power
    
    
    def GetPower(self):      
        if self.Simulation:
            Power = SimuTLS_Power
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TPDB?\n"
            self.Send(Command)
            Power = self.Receive()
        
        return self.ConvertForReading(float(Power[:-1]))
    
    
    def SetUnit(self, Unit):
        if not isinstance(Unit, str):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Unit")
            sys.exit()
        
        if Unit.lower() in self.ValidUnits:
            self.Unit = Unit
    
    
    def GetUnit(self):
        return self.Unit


    def On(self):
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:L1\n"
            self.Send(Command)
        self.Status = "ON"
        time.sleep(5)


    def Off(self):
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:L0\n"
            self.Send(Command)
        self.Status = "OFF"


    def GetStatus(self):
        return self.Status
        
        
    def SetWavelength(self, Wavelength):
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if Wavelength < AP1000_TLS_WLMIN[self.Type] or Wavelength > AP1000_TLS_WLMAX[self.Type]:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()
        
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TWL" + ("%4.3f" % Wavelength).zfill(8) + "\n"
            self.Send(Command)

        self.Wavelength = Wavelength
    
    
    def GetWavelength(self):
        if self.Simulation:
            Wavelength = SimuTLS_Wavelength
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TWL?\n"
            self.Send(Command)
            Wavelength = self.Receive()
            
        return float(Wavelength[:-1])
    
    
    def SetFrequency(self, Frequency):
        if not isinstance(Frequency, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Frequency")
            sys.exit()
            
        if Frequency > 0:
            self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency)
        else:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Frequency")
    
            
    def GetFrequency(self):
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
            
        Wavelength = self.GetWavelength()
        return VACCUM_LIGHT_SPEED / Wavelength
