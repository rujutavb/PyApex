

from PyApex.Common import Send, Receive


class TunableLaser():

    def __init__(self, Equipment, SlotNumber, Simulation=False):
        '''
        Constructor of a TLS (Tunable Laser Source) equipment.
        Equipement is the AP1000 class of the equipement
        SlotNumber is the number of the slot used by the TLS
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
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
        '''
        Return the equipement name and the slot number when the 'print()' function is used
        '''
        return "Tunable Laser in slot " + str(self.SlotNumber)


    def GetType(self):
        '''
        Return the type of the TLS
        return 0 for a C band Laser
        return 2 for a L band Laser
        '''
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
            self.Off()
            self.Connexion.close()
            raise ApexError(AP1000_ERROR_SLOT_TYPE_NOT_DEFINED, self.SlotNumber)
            
    
    def ConvertForWriting(self, Power):
        '''
        Internal use only
        Convert a dBm power in mW or a mW power in dBm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_VALUE, APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        from math import log10 as log
        
        if self.Unit.lower() == "dbm":
            return Power
        elif self.Unit.lower() == "mw":
            try:
                log(Power)
            except:
                self.Off()
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Power")
            else:
                return -10 * log(Power/100)
        else:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")


    def ConvertForReading(self, Power):
        '''
        Internal use only
        Convert a dBm power in mW or a mW power in dBm
        '''
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
        '''
        Set output power of the TLS equipment
        Power is expressed in the unit defined by the GetUnit() method
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_TLS_POWMIN, AP1000_TLS_POWMAX
        from PyApex.Errors import ApexError
        
        try:
            Power = float(Power)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Power")
        else:
            Power = self.ConvertForWriting(Power)
            if Power < AP1000_TLS_POWMIN[self.Type]:
                print("PyApex Warning. TLS Power is set to its minimum value: " + \
                      str(AP1000_TLS_POWMIN[self.Type]) + " dBm !")
                Power = AP1000_TLS_POWMIN[self.Type]
            elif Power > AP1000_TLS_POWMAX[self.Type]:
                print("PyApex Warning. TLS Power is set to its maximum value: " + \
                      str(AP1000_TLS_POWMIN[self.Type]) + " dBm !")
                Power = AP1000_TLS_POWMAX[self.Type]
                
            if self.Simulation:
                self.Power = Power
            else:
                Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TPDB" + \
                          ("%.1f" % Power) + "\n"
                Send(self.Connexion, Command)
                self.Power = Power


    def GetPower(self):
        '''
        Get output power of the TLS equipment
        The return power is expressed in the unit defined by the GetUnit() method
        '''
        from PyApex.Constantes import SimuTLS_Power
        
        if self.Simulation:
            Power = SimuTLS_Power
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TPDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return self.ConvertForReading(float(Power[:-1]))


    def SetUnit(self, Unit):
        '''
        Set the power unit of the TLS equipment
        Unit is a string which could be "dBm" for logaritmic or "mW" for linear power
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        
        try:
            Unit = str(Unit)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Unit")
        else:
            if Unit.lower() in self.ValidUnits:
                self.Unit = Unit


    def GetUnit(self):
        '''
        Get power unit of the TLS equipment
        The return unit is a string
        '''
        return self.Unit


    def On(self):
        '''
        Activate the output power of TLS equipment
        Waits 1 second after switching on
        '''
        from time import sleep
        
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:L1\n"
            Send(self.Connexion, Command)
        self.Status = "ON"
        sleep(1)


    def Off(self):
        '''
        Shut down the output power of the TLS equipment
        '''
        if not self.Simulation:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:L0\n"
            Send(self.Connexion, Command)
        self.Status = "OFF"


    def GetStatus(self):
        '''
        Return the status ("ON" or "OFF") of the TLS equipment
        '''
        return self.Status


    def SetWavelength(self, Wavelength):
        '''
        Set wavelength of the TLS equipment
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_TLS_WLMIN, AP1000_TLS_WLMAX
        from PyApex.Errors import ApexError
        
        try:
            Wavelength = float(Wavelength)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
        else:
            if Wavelength < AP1000_TLS_WLMIN[self.Type]:
                print("PyApex Warning. TLS Wavelength is set to its minimum value: " + \
                      str(AP1000_TLS_WLMIN[self.Type]) + " nm !")
                Wavelength = AP1000_TLS_WLMIN[self.Type]
            if Wavelength > AP1000_TLS_WLMAX[self.Type]:
                print("PyApex Warning. TLS Wavelength is set to its maximum value: " + \
                      str(AP1000_TLS_WLMAX[self.Type]) + " nm !")
                Wavelength = AP1000_TLS_WLMAX[self.Type]
            
            if not self.Simulation:
                Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TWL" + \
                          ("%4.3f" % Wavelength).zfill(8) + "\n"
                Send(self.Connexion, Command)
            
            self.Wavelength = Wavelength


    def GetWavelength(self):
        '''
        Get wavelength of the TLS equipment
        The return wavelength is expressed in nm
        '''
        from PyApex.Constantes import SimuTLS_Wavelength
        
        if self.Simulation:
            Wavelength = SimuTLS_Wavelength
        else:
            Command = "TLS[" + str(self.SlotNumber).zfill(2) + "]:TWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)
            
        return float(Wavelength[:-1])


    def SetFrequency(self, Frequency):
        '''
        Set frequency of the TLS equipment
        Frequency is expressed in GHz
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import VACCUM_LIGHT_SPEED, AP1000_TLS_WLMAX
        from PyApex.Errors import ApexError
        
        try:
            Frequency = float(Frequency)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Frequency")
        else:
            if Frequency > 0:
                self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency)
            else:
                print("PyApex Warning. TLS Frequency is set to its minimum value: " + \
                      str(AP1000_TLS_WLMAX[self.Type] / VACCUM_LIGHT_SPEED) + " GHz !")
                self.SetWavelength(AP1000_TLS_WLMAX[self.Type])


    def GetFrequency(self):
        '''
        Get frequency of the TLS equipment
        The return frequency is expressed in GHz
        '''
        from PyApex.Constantes import VACCUM_LIGHT_SPEED
            
        Wavelength = self.GetWavelength()
        return VACCUM_LIGHT_SPEED / Wavelength
