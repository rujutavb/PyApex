from PyApex.Common import Send, Receive


class Attenuator():

    def __init__(self, Equipment, SlotNumber=1, Simulation=False):
        '''
        Constructor of a ATT (Attenuator) equipment.
        Equipement is the AP1000 class of the equipement
        SlotNumber is the number of the slot used by the ATT
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.SlotNumber = SlotNumber
        self.Unit = "dB"
        self.Attenuation = 0
        self.ValidUnits = ["db", "%"]


    def __str__(self):
        '''
        Return the equipement name and the slot number when the 'print()' function is used
        '''
        return "Optical Attenuator in slot " + str(self.SlotNumber)


    def ConvertForWriting(self, Attenuation):
        '''
        Internal use only
        Convert a dB attenuation in % or a % attenuation in dB
        '''
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
        '''
        Internal use only
        Convert a dB attenuation in % or a % attenuation in dB
        '''
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
        '''
        Set attenuation power of the ATT equipment
        Attenuation is expressed in the unit defined by the GetUnit() method
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_ATT_ATTMIN, AP1000_ATT_ATTMAX, AP1000_ATT_CHNUMBER
        from PyApex.Errors import ApexError
        
        try:
            Attenuation = float(Attenuation)
        except:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Attenuation")
        else:
            try:
                ChNumber = int(ChNumber)
            except:
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
            else:
                
                Attenuation = self.ConvertForWriting(Attenuation)
                if Attenuation < AP1000_ATT_ATTMIN:
                    Attenuation = AP1000_ATT_ATTMIN
                if Attenuation > AP1000_ATT_ATTMAX:
                    Attenuation = AP1000_ATT_ATTMAX
                if ChNumber > AP1000_ATT_CHNUMBER:
                    ChNumber = AP1000_ATT_CHNUMBER
                if ChNumber < 1:
                    ChNumber = 1
                
                if self.Simulation:
                    self.Attenuation = Attenuation
                else:
                    Command = "ATT[" + str(self.SlotNumber).zfill(2) + "]:DB[" + \
                              str(ChNumber-1) +"]" + ("%.1f" % Attenuation) + "\n"
                    Send(self.Connexion, Command)
            self.Attenuation = Attenuation


    def GetAttenuation(self, ChNumber=1):
        '''
        Get attenuation of the ATT equipment
        The return attenuation is expressed in the unit defined by the GetUnit() method
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_ATT_CHNUMBER, SimuATT_Attenuation
        from PyApex.Errors import ApexError
        
        try:
            ChNumber = int(ChNumber)
        except:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        else:
            
            if ChNumber > AP1000_ATT_CHNUMBER:
                ChNumber = AP1000_ATT_CHNUMBER
            if ChNumber < 1:
                ChNumber = 1
            
            if self.Simulation:
                Attenuation = SimuATT_Attenuation
            else:
                Command = "ATT[" + str(self.SlotNumber).zfill(2) + "]:DB[" + \
                          str(ChNumber-1) + "]?\n"
                Send(self.Connexion, Command)
                Attenuation = Receive(self.Connexion)
            
            return self.ConvertForReading(float(Attenuation[:-1]))


    def SetUnit(self, Unit):
        '''
        Set the attenuation unit of the ATT equipment
        Unit is a string which could be "dB" for logaritmic or "%" for linear power
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        
        try:
            Unit = str(Unit)
        except:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Unit")
        else:
            if Unit.lower() in self.ValidUnits:
                self.Unit = Unit


    def GetUnit(self):
        '''
        Get the attenuation unit of the ATT equipment
        Unit is a string which could be "dB" for logaritmic or "%" for linear power
        '''
        return self.Unit
