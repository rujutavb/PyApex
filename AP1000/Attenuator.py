

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

        
    def Send(self, Command):
        from PyApex.Constantes import AP1000_ERROR_ARGUMENT_TYPE, AP1000_ERROR_BADCOMMAND
        from PyApex.Errors import ApexError
        from sys import exit
        
        if not isinstance(Command, str):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Command")
            sys.exit()
        try:
            self.Connexion.send(Command.encode('utf-8'))
        except:
            raise ApexError(AP1000_ERROR_BADCOMMAND, Command)
            sys.exit()


    def Receive(self, ByteNumber=1024):
        from PyApex.Constantes import AP1000_ERROR_ARGUMENT_TYPE, AP1000_ERROR_COMMUNICATION
        from PyApex.Errors import ApexError
        from sys import exit
        
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
            
    
    def ConvertForWriting(self, Attenuation):
        from PyApex.Constantes import AP1000_ERROR_ARGUMENT_VALUE, AP1000_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        from sys import exit
        from math import log10 as log
        
        if self.Unit.lower() == "db":
            return Attenuation
        elif self.Unit.lower() == "%":
            try:
                log(Attenuation)
            except:
                raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Attenuation")
                sys.exit()
            else:
                return -10 * log(Attenuation/100)
        else:
            raise ApexError(AP1000_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
            sys.exit()


    def ConvertForReading(self, Attenuation):
        from PyApex.Constantes import AP1000_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        from sys import exit
        
        if self.Unit.lower() == "%":
            return 10**(- Attenuation / 10)
        elif self.Unit.lower() == "db":
            return Attenuation
        else:
            raise ApexError(AP1000_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
            sys.exit()
    
    
    def SetAttenuation(self, Attenuation, ChNumber=1):
        from PyApex.Constantes import AP1000_ERROR_ARGUMENT_TYPE, AP1000_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        from sys import exit
        
        if not isinstance(Attenuation, (float, int)):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Attenuation")
            sys.exit()
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
            
        Attenuation = self.ConvertForWriting(Attenuation)
        if Attenuation < AP1000_ATT_ATTMIN or Attenuation > AP1000_ATT_ATTMAX:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "Attenuation")
            sys.exit()
        if ChNumber > AP1000_ATT_CHNUMBER or ChNumber < 1:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
            
        if self.Simulation:
            self.Attenuation = Attenuation
        else:
            Command = "ATT[" + str(self.SlotNumber).zfill(2) + "]:DB[" + str(ChNumber-1) +"]" + ("%.1f" % Attenuation) + "\n"
            self.Send(Command)
            self.Attenuation = Attenuation
    
    
    def GetAttenuation(self, ChNumber=1):
        from PyApex.Constantes import AP1000_ERROR_ARGUMENT_TYPE, AP1000_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        from sys import exit
        
        if not isinstance(ChNumber, int):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "ChNumber")
            sys.exit()
        if ChNumber > AP1000_ATT_CHNUMBER or ChNumber < 1:
            raise ApexError(AP1000_ERROR_ARGUMENT_VALUE, "ChNumber")
            sys.exit()
        
        if self.Simulation:
            Attenuation = SimuATT_Attenuation
        else:
            Command = "ATT[" + str(self.SlotNumber).zfill(2) + "]:DB[" + str(ChNumber-1) + "]?\n"
            self.Send(Command)
            Attenuation = self.Receive()
        
        return self.ConvertForReading(float(Attenuation[:-1]))
    
    
    def SetUnit(self, Unit):
        from PyApex.Constantes import AP1000_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        from sys import exit
        
        if not isinstance(Unit, str):
            raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Unit")
            sys.exit()
        
        if Unit.lower() in self.ValidUnits:
            self.Unit = Unit
    
    
    def GetUnit(self):
        return self.Unit
