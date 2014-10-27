from PyApex.Constantes import *
from PyApex.Errors import ApexError


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
            if data.decode('utf-8')[:-1] == "BAD COMMAND":
                raise ApexError(AP1000_ERROR_BADCOMMAND, "Reception after last command")
                sys.exit()
            return data.decode('utf-8')


    def GetChannels(self):
        if self.Simulation:
            ID = SimuPWM_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            self.Send(Command)
            ID = self.Receive()
        
        Channels = []
        for c in ID.split("/")[2].split("-")[3]:
            for k, v in AP1000_PWM_CHTYPE.items():
                if c == k:
                    Channels.append(v)
        
        return Channels
            
    
    def SetAverageTime(self, AvgTime):
        if not isinstance(AvgTime, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "AvgTime")
            sys.exit()
        if AvgTime < AP1000_PWM_AVGMIN or AvgTime > AP1000_PWM_AVGMAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "AvgTime")
            sys.exit()
            
        if self.Simulation:
            self.AvgTime = AvgTime
        else:
            Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:SETAVERAGE" + str(AvgTime) + "\n"
            self.Send(Command)
            self.AvgTime = AvgTime
    
    
    def GetAverageTime(self):
        if self.Simulation:
            AvgTime = SimuPWM_AvgTime
        else:
            Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:SETAVERAGE?\n"
            self.Send(Command)
            AvgTime = self.Receive()
            
        return float(AvgTime[:-1])
    
    
    def SetUnit(self, Unit):
        if not isinstance(Unit, str):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Unit")
            sys.exit()
        
        if Unit.lower() in self.ValidUnits:
            self.Unit = Unit
    
    
    def GetUnit(self):
        return self.Unit
        
        
    def SetWavelength(self, Wavelength, ChNumber=1):
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
        if Wavelength < AP1000_PWM_WLMIN or Wavelength > AP1000_PWM_WLMAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()
        if ChNumber > len(self.Channels):
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
        
        if not self.Simulation:
            Command = "POW[" + str(self.SlotNumber).zfill(2) + \
                    "]:SETWAVELENGTH[" + str(ChNumber) + "]" + ("%4.3f" % Wavelength).zfill(8) + "\n"
            self.Send(Command)
    
    
    def GetWavelength(self, ChNumber=1):
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
        if ChNumber > len(self.Channels):
            raise APexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
        
        if self.Simulation:
            Wavelength = SimuPWM_Wavelength
        else:
            Command = "POW[" + str(slef.SlotNumber).zfill(2) + "]:WAV[" + str(ChNumber) + "]?\n"
            self.Send(Command)
            Wavelength = self.Receive()
            
        return float(Wavelength[:-1])
    
    
    def SetFrequency(self, Frequency, ChNumber=1):
        if not isinstance(Frequency, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Frequency")
            sys.exit()
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
        if ChNumber > len(self.Channels):
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
            
        if Frequency > 0:
            self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency, ChNumber)
        else:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Frequency")
    
            
    def GetFrequency(self, ChNumber=1):
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
        if ChNumber > len(self.Channels):
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
            
        Wavelength = self.GetWavelength(ChNumber)
        return float(VACCUM_LIGHT_SPEED / Wavelength)
    
    
    def GetPower(self, ChNumber=1):
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
        if ChNumber > len(self.Channels):
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
        
        if self.Simulation:
            if self.Unit.lower() == "dbm":
                Power = SimuPWM_Power_dBm
            elif self.Unit.lower() == "mw":
                Power = SimuPWM_Power_mW
            else:
                raise ApexError(AP1000_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
                sys.exit()
        else:
            if self.Unit.lower() == "dbm":
                Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:DBM[" + str(ChNumber) + "]?\n"
            elif self.Unit.lower() == "mw":
                Command = "POW[" + str(self.SlotNumber).zfill(2) + "]:MW[" + str(ChNumber) + "]?\n"
            else:
                raise ApexError(AP1000_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
                sys.exit()
            self.Send(Command)
            Power = self.Receive()
            
        return float(Power[:-1])
