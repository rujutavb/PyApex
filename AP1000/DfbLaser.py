

from PyApex.Common import Send, Receive


class DfbLaser():

    def __init__(self, Equipment, SlotNumber, Simulation=False):
        '''
        Constructor of a DFB (Distributed FeedBack Laser Source) equipment.
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
        Return the type of the DFB
        return 0 for a C band Laser
        return 2 for a L band Laser
        return 5 for a O band Laser
        '''
        from PyApex.Constantes import AP1000_ERROR_SLOT_TYPE_NOT_DEFINED
        from PyApex.Constantes import SimuDFB_SlotID, AP1000_DFB_CBAND, AP1000_DFB_LBAND, AP1000_DFB_OBAND
        from PyApex.Errors import ApexError
        import re
        
        if self.Simulation:
            ID = SimuDFB_SlotID
        else:
            Command = "SLT[" + str(self.SlotNumber).zfill(2) + "]:IDN?\n"
            Send(self.Connexion, Command)
            ID = Receive(self.Connexion)

        if re.findall(str(AP1000_DFB_CBAND), ID.split("/")[1]) != []:
            return 0
        elif re.findall(str(AP1000_DFB_LBAND), ID.split("/")[1]) != []:
            return 2
        elif re.findall(str(AP1000_DFB_OBAND), ID.split("/")[1]) != []:
            return 5
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
        Set output power of the DFB equipment
        Power is expressed in the unit defined by the GetUnit() method
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_DFB_POWMIN, AP1000_DFB_POWMAX
        from PyApex.Errors import ApexError
        
        try:
            Power = float(Power)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Power")
        else:
            Power = self.ConvertForWriting(Power)
            if Power < AP1000_DFB_POWMIN[self.Type]:
                print("PyApex Warning. DFB Power is set to its minimum value: " + \
                      str(AP1000_DFB_POWMIN[self.Type]) + " dBm !")
                Power = AP1000_DFB_POWMIN[self.Type]
            elif Power > AP1000_DFB_POWMAX[self.Type]:
                print("PyApex Warning. DFB Power is set to its maximum value: " + \
                      str(AP1000_DFB_POWMAX[self.Type]) + " dBm !")
                Power = AP1000_DFB_POWMAX[self.Type]
                
            if self.Simulation:
                self.Power = Power
            else:
                Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:TPDB" + \
                          ("%.1f" % Power) + "\n"
                Send(self.Connexion, Command)
                self.Power = Power


    def GetPower(self):
        '''
        Get output power of the DFB equipment
        The return power is expressed in the unit defined by the GetUnit() method
        '''
        from PyApex.Constantes import AP1000_DFB_POWMIN, AP1000_DFB_POWMAX
        from random import random
        
        if self.Simulation:
            self.Power = random() * (AP1000_DFB_POWMAX[self.Type] - AP1000_DFB_POWMIN[self.Type]) + AP1000_DFB_POWMIN[self.Type]
        else:
            Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:TPDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
            self.Power = float(Power[:-1])
        
        return self.ConvertForReading(self.Power)


    def SetUnit(self, Unit):
        '''
        Set the power unit of the DFB equipment
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
        Get power unit of the DFB equipment
        The return unit is a string
        '''
        return self.Unit


    def On(self):
        '''
        Activate the output power of DFB equipment
        Waits 0.2 second after switching on
        '''
        from time import sleep
        
        if not self.Simulation:
            Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:L1\n"
            Send(self.Connexion, Command)
        self.Status = "ON"
        sleep(0.2)


    def Off(self):
        '''
        Shut down the output power of the DFB equipment
        '''
        if not self.Simulation:
            Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:L0\n"
            Send(self.Connexion, Command)
        self.Status = "OFF"


    def GetStatus(self):
        '''
        Return the status ("ON" or "OFF") of the DFB equipment
        '''
        
        if not self.Simulation:
            Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:L?\n"
            Send(self.Connexion, Command)
            StrStatus = Receive(self.Connexion)[:-1]
        
            if StrStatus == "1":
                self.Status = "ON"
            else:
                self.Status = "OFF"
                
        return self.Status


    def SetWavelength(self, Wavelength):
        '''
        Set wavelength of the DFB equipment
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_DFB_WLMIN, AP1000_DFB_WLMAX
        from PyApex.Errors import ApexError
        
        try:
            Wavelength = float(Wavelength)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
        else:
            if Wavelength < AP1000_DFB_WLMIN[self.Type]:
                print("PyApex Warning. DFB Wavelength is set to its minimum value: " + \
                      str(AP1000_DFB_WLMIN[self.Type]) + " nm !")
                Wavelength = AP1000_DFB_WLMIN[self.Type]
            if Wavelength > AP1000_DFB_WLMAX[self.Type]:
                print("PyApex Warning. DFB Wavelength is set to its maximum value: " + \
                      str(AP1000_DFB_WLMAX[self.Type]) + " nm !")
                Wavelength = AP1000_DFB_WLMAX[self.Type]
            
            if not self.Simulation:
                Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:TWL" + \
                          ("%4.3f" % Wavelength).zfill(8) + "\n"
                Send(self.Connexion, Command)
            
            self.Wavelength = Wavelength


    def GetWavelength(self):
        '''
        Get wavelength of the DFB equipment
        The return wavelength is expressed in nm
        '''
        from PyApex.Constantes import AP1000_DFB_WLMIN, AP1000_DFB_WLMAX
        from random import random
        
        if self.Simulation:
            Wavelength = random() * (AP1000_DFB_WLMAX[self.Type] - AP1000_DFB_WLMIN[self.Type]) + AP1000_DFB_WLMIN[self.Type]
        else:
            Command = "DFB[" + str(self.SlotNumber).zfill(2) + "]:TWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)
        
        try:
            self.Wavelength = float(Wavelength[:-1])
        except:
            pass
            
        return self.Wavelength


    def SetFrequency(self, Frequency):
        '''
        Set frequency of the DFB equipment
        Frequency is expressed in GHz
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import VACCUM_LIGHT_SPEED, AP1000_DFB_FRMIN, AP1000_DFB_FRMAX
        from PyApex.Errors import ApexError
        
        try:
            Frequency = float(Frequency)
        except:
            self.Off()
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Frequency")
        else:
            if Frequency < AP1000_DFB_FRMIN[self.Type]:
                print("PyApex Warning. DFB Frequency is set to its minimum value: " + \
                      str(AP1000_DFB_FRMIN[self.Type]) + " nm !")
                Frequency = AP1000_DFB_FRMIN[self.Type]
            if Frequency > AP1000_DFB_FRMAX[self.Type]:
                print("PyApex Warning. DFB Frequency is set to its maximum value: " + \
                      str(AP1000_DFB_FRMAX[self.Type]) + " nm !")
                Frequency = AP1000_DFB_FRMAX[self.Type]
            
            self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency)


    def GetFrequency(self):
        '''
        Get frequency of the DFB equipment
        The return frequency is expressed in GHz
        '''
        from PyApex.Constantes import VACCUM_LIGHT_SPEED
            
        Wavelength = self.GetWavelength()
        return VACCUM_LIGHT_SPEED / Wavelength
    
    
