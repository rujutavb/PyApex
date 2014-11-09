

from PyApex.Common import Send, Receive


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


    def GetType(self):
        from PyApex.Constantes import AP1000_ERROR_SLOT_TYPE_NOT_DEFINED
        from PyApex.Constantes import SimuTLS_SlotID, AP1000_TLS_CBAND, AP1000_TLS_LBAND
        from PyApex.Errors import ApexError
        import re
        
        if self.Simulation:
            ID = SimuTLS_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            Send(self.Connexion, Command)
            ID = Receive(self.Connexion)

        if re.findall(str(AP1000_TLS_CBAND), ID.split("/")[1]) != []:
            return 0
        elif re.findall(str(AP1000_TLS_CLBAND), ID.split("/")[1]) != []:
            return 2
        else:
            self.Connexion.close()
            raise ApexError(AP1000_ERROR_SLOT_TYPE_NOT_DEFINED, self.SlotNumber)
            
    
    def ConvertForWriting(self, Power):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_VALUE, APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        from math import log10 as log
        
        if self.Unit.lower() == "dbm":
            return Power
        elif self.Unit.lower() == "mw":
            try:
                log(Power)
            except:
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Power")
            else:
                return -10 * log(Power/100)
        else:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")


    def ConvertForReading(self, Power):
        from PyApex.Constantes import APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        
        if self.Unit.lower() == "mw":
            return 10**(Power / 10)
        elif self.Unit.lower() == "dbm":
            return Power
        else:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
    
    
    def SetPower(self, Power):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_TLS_POWMIN, AP1000_TLS_POWMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(Power, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Power")
            
        Power = self.ConvertForWriting(Power)
        if Power < AP1000_TLS_POWMIN[self.Type] or Power > AP1000_TLS_POWMAX[self.Type]:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Power")
            
        if self.Simulation:
            self.Power = Power
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TPDB" + ("%.1f" % Power) + "\n"
            Send(self.Connexion, Command)
            self.Power = Power
    
    
    def GetPower(self):
        from PyApex.Constantes import SimuTLS_Power
        
        if self.Simulation:
            Power = SimuTLS_Power
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TPDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return self.ConvertForReading(float(Power[:-1]))
    
    
    def SetUnit(self, Unit):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        
        if not isinstance(Unit, str):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Unit")
        
        if Unit.lower() in self.ValidUnits:
            self.Unit = Unit
    
    
    def GetUnit(self):
        return self.Unit


    def On(self):
        from time import sleep
        
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:L1\n"
            Send(self.Connexion, Command)
        self.Status = "ON"
        sleep(5)


    def Off(self):
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:L0\n"
            Send(self.Connexion, Command)
        self.Status = "OFF"


    def GetStatus(self):
        return self.Status
        
        
    def SetWavelength(self, Wavelength):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_TLS_WLMIN, AP1000_TLS_WLMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(Wavelength, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
        if Wavelength < AP1000_TLS_WLMIN[self.Type] or Wavelength > AP1000_TLS_WLMAX[self.Type]:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
        
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TWL" + ("%4.3f" % Wavelength).zfill(8) + "\n"
            Send(self.Connexion, Command)

        self.Wavelength = Wavelength
    
    
    def GetWavelength(self):
        from PyApex.Constantes import SimuTLS_Wavelength
        
        if self.Simulation:
            Wavelength = SimuTLS_Wavelength
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)
            
        return float(Wavelength[:-1])
    
    
    def SetFrequency(self, Frequency):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import VACCUM_LIGHT_SPEED
        from PyApex.Errors import ApexError
        
        if not isinstance(Frequency, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Frequency")
            
        if Frequency > 0:
            self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency)
        else:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Frequency")
    
            
    def GetFrequency(self):
        from PyApex.Constantes import VACCUM_LIGHT_SPEED
            
        Wavelength = self.GetWavelength()
        return VACCUM_LIGHT_SPEED / Wavelength
