

from PyApex.Common import Send, Receive


class PowerMeter():

    def __init__(self, Equipment, SlotNumber=1, Simulation=False):
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.SlotNumber = SlotNumber
        self.Unit = "dBm"
        self.Wavelength = 1550
        self.AvgTime = 100
        self.Channels = self.GetChannels()
        self.ValidUnits = ["dbm", "mw"]
        
       
    def __str__(self):
        return "Optical Power Meter in slot " + str(self.SlotNumber)


    def GetChannels(self):
        from PyApex.Constantes import AP1000_PWM_CHTYPE
        
        if self.Simulation:
            ID = SimuPWM_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            Send(self.Connexion, Command)
            ID = Receive(self.Connexion)
        
        Channels = []
        for c in ID.split("/")[2].split("-")[3]:
            for k, v in AP1000_PWM_CHTYPE.items():
                if c == k:
                    Channels.append(v)
        
        return Channels
            
    
    def SetAverageTime(self, AvgTime):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_PWM_AVGMIN, AP1000_PWM_AVGMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(AvgTime, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "AvgTime")
        if AvgTime < AP1000_PWM_AVGMIN or AvgTime > AP1000_PWM_AVGMAX:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "AvgTime")
            
        if self.Simulation:
            self.AvgTime = AvgTime
        else:
            Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:SETAVERAGE" + str(AvgTime) + "\n"
            Send(self.Connexion, Command)
            self.AvgTime = AvgTime
    
    
    def GetAverageTime(self):
        if self.Simulation:
            AvgTime = SimuPWM_AvgTime
        else:
            Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:SETAVERAGE?\n"
            Send(self.Connexion, Command)
            AvgTime = Receive(self.Connexion)
            
        return float(AvgTime[:-1])
    
    
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
        
        
    def SetWavelength(self, Wavelength, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_PWM_WLMIN, AP1000_PWM_WLMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(Wavelength, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        if Wavelength < AP1000_PWM_WLMIN or Wavelength > AP1000_PWM_WLMAX:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
        if ChNumber > len(self.Channels):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
        
        if not self.Simulation:
            Command = "POW[" + str(self.SlotNumber).zfill(2) + \
                    "]:SETWAVELENGTH[" + str(ChNumber) + "]" + ("%4.3f" % Wavelength).zfill(8) + "\n"
            Send(self.Connexion, Command)
    
    
    def GetWavelength(self, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        if ChNumber > len(self.Channels):
            self.Connexion.close()
            raise APexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
        
        if self.Simulation:
            Wavelength = SimuPWM_Wavelength
        else:
            Command = "POW[" + str(slef.SlotNumber).zfill(2) + "]:WAV[" + str(ChNumber) + "]?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)
            
        return float(Wavelength[:-1])
    
    
    def SetFrequency(self, Frequency, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        
        if not isinstance(Frequency, (float, int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Frequency")
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        if ChNumber > len(self.Channels):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
            
        if Frequency > 0:
            self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency, ChNumber)
        else:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Frequency")
    
            
    def GetFrequency(self, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        if ChNumber > len(self.Channels):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
            
        Wavelength = self.GetWavelength(ChNumber)
        return float(VACCUM_LIGHT_SPEED / Wavelength)
    
    
    def GetPower(self, ChNumber=1):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        
        if not isinstance(ChNumber, int):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        if ChNumber > len(self.Channels):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ChNumber")
        
        if self.Simulation:
            if self.Unit.lower() == "dbm":
                Power = SimuPWM_Power_dBm
            elif self.Unit.lower() == "mw":
                Power = SimuPWM_Power_mW
            else:
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
        else:
            if self.Unit.lower() == "dbm":
                Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:DBM[" + str(ChNumber) + "]?\n"
            elif self.Unit.lower() == "mw":
                Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:MW[" + str(ChNumber) + "]?\n"
            else:
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
            
        return float(Power[:-1])
