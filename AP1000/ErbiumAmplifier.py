from PyApex.Common import Send, Receive


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


    def GetType(self):
        from PyApex.Constantes import AP1000_ERROR_SLOT_TYPE_NOT_DEFINED
        from PyApex.Constantes import SimuEFA_SlotID
        from PyApex.Errors import ApexError
        import re
        
        if self.Simulation:
            ID = SimuEFA_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            Send(self.Connexion, Command)
            ID = Receive(self.Connexion)

        if re.findall("A", ID.split("/")[2].split("-")[2]) != []:
            return 0
        elif re.findall("B", ID.split("/")[2].split("-")[2]) != []:
            return 1
        elif re.findall("C", ID.split("/")[2].split("-")[2]) != []:
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


    def GetInVoltage(self):
        from PyApex.Constantes import SimuEFA_InVoltage
        
        if self.Simulation:
            InVoltage = SimuEFA_InVoltage
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:POWERINVALUE\n"
            Send(self.Connexion, Command)
            InVoltage = Receive(self.Connexion)

        return int(InVoltage[:-1])


    def GetOutVoltage(self):
        from PyApex.Constantes import SimuEFA_OutVoltage
        
        if self.Simulation:
            InVoltage = SimuEFA_OutVoltage
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:POWEROUTVALUE\n"
            Send(self.Connexion, Command)
            InVoltage = Receive(self.Connexion)

        return int(InVoltage[:-1])


    def SetIPump(self, IPump):
        from PyApex.Constantes import APXXXX_ERROR__ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyAPex.Constantes import AP1000_EFA_IPMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(IPump, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR__ARGUMENT_TYPE, "IPump")
        if IPump > AP1000_EFA_IPMAX[self.Type] or IPump < 0:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "IPump")

        if not self.Simulation:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:PUMP" + ("%.1f" % IPump) + "\n"
            Send(self.Connexion, Command)

        self.IPump = IPump
    
    
    def GetInPower(self):
        from PyApex.Constantes import SimuEFA_InPower
        
        if self.Simulation:
            Power = SimuEFA_InPower
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:INDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return float(Power[:-1])


    def GetOutPower(self):
        from PyApex.Constantes import SimuEFA_OutPower
        
        if self.Simulation:
            Power = SimuEFA_OutPower
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:OTDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return float(Power[:-1])
    
    
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
