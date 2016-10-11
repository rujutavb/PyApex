from PyApex.Common import Send, Receive


class Filter():

    def __init__(self, Equipment, SlotNumber=1, Simulation=False):
        '''
        Constructor of a FIL (Filter) equipment.
        Equipement is the AP1000 class of the equipement
        SlotNumber is the number of the slot used by the FIL
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.SlotNumber = SlotNumber
        self.Unit = "nm"
        self.Wavelength = 1550.0
        self.ValidUnits = ["nm", "ghz"]


    def __str__(self):
        '''
        Return the equipement name and the slot number when the 'print()' function is used
        '''
        return "Optical Filter in slot " + str(self.SlotNumber)


    def Convert(self, Value):
        '''
        Internal use only
        Convert a wavelength (nm) in frequency (GHz) or a frequency (GHz) in wavelength (nm)
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_VALUE, APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Constantes import Celerity
        from PyApex.Errors import ApexError
        
        return Celerity / Value


    def SetWavelength(self, Wavelength):
        '''
        Set Wavelength of the FIL equipment
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_FIL_WLMIN, AP1000_FIL_WLMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(Wavelength, (int, float)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        
        [WavelengthMin, WavelengthMax] = self.GetWavelngthLimits()
        if(Wavelength < WavelengthMin or Wavelength > WavelengthMax):
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()
            
        if not self.Simulation:
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:TWL" + \
                      ("%.3f" % Wavelength) + "\n"
            Send(self.Connexion, Command)
        
        self.Wavelength = Wavelength


    def GetWavelength(self):
        '''
        Get Wavelength of the FIL equipment
        Returns the wavelength in nm
        '''
                           
        if self.Simulation:
            Wavelength = self.Wavelength
        else:
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:TWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)
        
        return float(Wavelength[:-1])
        

    def SetFrequency(self, Frequency):
        '''
        Set Frequency of the FIL equipment
        Frequency is expressed in GHz
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        
        if not isinstance(Frequency, (int, float)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Frequency")
            sys.exit()
        
        [FrequencyMin, FrequencyMax] = self.GetFrequencyLimits()
        if(Frequency < FrequencyMin or Frequency > FrequencyMax):
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Frequency")
            sys.exit()
            
        if not self.Simulation:
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:TFR" + \
                      ("%.3f" % Frequency) + "\n"
            Send(self.Connexion, Command)
        
        
        self.Wavelength = self.Convert(Frequency)


    def GetFrequency(self):
        '''
        Get Frequency of the FIL equipment
        Returns the Frequency in GHz
        '''
        
        if self.Simulation:
            Wavelength = self.Wavelength
        else:
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:TFR?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)
        
        return float(Wavelength[:-1])
    
    
    def GetWavelngthLimits(self):
        '''
        Get the wavelength limits (min and max) of the FIL equipment
        Returns the limits in nm in a list [min, max]
        '''
        from PyApex.Constantes import AP1000_FIL_WLMIN, AP1000_FIL_WLMAX
        from PyApex.Errors import ApexError
        
        if self.Simulation:
            WavelengthMin = AP1000_FIL_WLMIN
            WavelengthMax = AP1000_FIL_WLMAX
        else:
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:WLMIN?\n"
            Send(self.Connexion, Command)
            WavelengthMin = float(Receive(self.Connexion)[:-1])
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:WLMAX?\n"
            Send(self.Connexion, Command)
            WavelengthMax = float(Receive(self.Connexion)[:-1])
        
        return [WavelengthMin, WavelengthMax]
        
        
    def GetFrequencyLimits(self):
        '''
        Get the frequency limits (min and max) of the FIL equipment
        Returns the limits in GHz in a list [min, max]
        '''
        from PyApex.Constantes import AP1000_FIL_FRMIN, AP1000_FIL_FRMAX
        from PyApex.Errors import ApexError
        
        if self.Simulation:
            FrequencyMin = AP1000_FIL_FRMIN
            FrequencyMax = AP1000_FIL_FRMAX
        else:
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:FRMIN?\n"
            Send(self.Connexion, Command)
            FrequencyMin = float(Receive(self.Connexion)[:-1])
            Command = "FIL[" + str(self.SlotNumber).zfill(2) + "]:FRMAX?\n"
            Send(self.Connexion, Command)
            FrequencyMax = float(Receive(self.Connexion)[:-1])
        
        return [FrequencyMin, FrequencyMax]


    def SetUnit(self, Unit):
        '''
        Set the unit of the FIL equipment
        Unit is a string which could be "nm" for wavelength or "GHz" for frequency
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        
        if not isinstance(Unit, str):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Unit")
            sys.exit()
        
        if Unit.lower() in self.ValidUnits:
            self.Unit = Unit


    def GetUnit(self):
        '''
        Get the unit of the FIL equipment
        Unit is a string which could be "nm" for wavelength or "GHz" for frequency
        '''
        return self.Unit
