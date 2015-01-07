from PyApex.Common import Send, Receive


class Attenuator():

    def __init__(self, Equipment, SlotNumber=1, Simulation=False):
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.SlotNumber = SlotNumber
        self.Unit = "dB"
        self.Attenuation = 0
        self.ValidUnits = ["db", "%"]
        
       
    def __str__(self):
        return "Optical Attenuator in slot " + str(self.SlotNumber)
   
    
    def ConvertForWriting(self, Attenuation):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_VALUE, APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        from math import log10 as log
        
        if self.Unit.lower() == "db":
            return Attenuation
        elif self.Unit.lower() == "%":
            try:
                log(Attenuation)
            except:
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Attenuation")
            else:
                return -10 * log(Attenuation/100)
        else:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")


    def ConvertForReading(self, Attenuation):
        from PyApex.Constantes import APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        
        if self.Unit.lower() == "%":
            return 10**(- Attenuation / 10)
        elif self.Unit.lower() == "db":
            return Attenuation
        else:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
    
    
    def SetAttenuation(self, Attenuation, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_ATT_ATTMIN, AP1000_ATT_ATTMAX, AP1000_ATT_CHNUMBER
        from PyApex.Errors import ApexError
        
        if not isinstance(Attenuation, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Attenuation")
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
            
        Attenuation = self.ConvertForWriting(Attenuation)
        if Attenuation < AP1000_ATT_ATTMIN or Attenuation > AP1000_ATT_ATTMAX:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Attenuation")
        if ChNumber > AP1000_ATT_CHNUMBER or ChNumber < 1:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
            
        if self.Simulation:
            self.Attenuation = Attenuation
        else:
            Command = "ATT[" + str(self.SlotNumber).zfill(2) + "]:DB[" + str(ChNumber-1) +"]" + ("%.1f" % Attenuation) + "\n"
            Send(self.Connexion, Command)
            self.Attenuation = Attenuation
    
    
    def GetAttenuation(self, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_ATT_CHNUMBER, SimuATT_Attenuation
        from PyApex.Errors import ApexError
        
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        if ChNumber > AP1000_ATT_CHNUMBER or ChNumber < 1:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
        
        if self.Simulation:
            Attenuation = SimuATT_Attenuation
        else:
            Command = "ATT[" + str(self.SlotNumber).zfill(2) + "]:DB[" + str(ChNumber-1) + "]?\n"
            Send(self.Connexion, Command)
            Attenuation = Receive(self.Connexion)
        
        return self.ConvertForReading(float(Attenuation[:-1]))
    
    
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
