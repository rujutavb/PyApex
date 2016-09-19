from PyApex.Common import Send, Receive


class ErbiumAmplifier():

    def __init__(self, Equipment, SlotNumber, Simulation=False):
        '''
        Constructor of a EFA (Erbium Amplifier) equipment.
        Equipement is the AP1000 class of the equipement
        SlotNumber is the number of the slot used by the EFA
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
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
        '''
        Return the equipement name and the slot number when the 'print()' function is used
        '''
        return "Erbium Amplifier in slot " + str(self.SlotNumber)


    def GetType(self, type="d"):
        '''
        Return the type of the EFA
        if type = 'd' (default), return a digit :
            - 0 for Booster
            - 1 for In-Line
            - 2 for Pre-Ampli
        if type = 'c', return the option character :
            - 'A' for Booster
            - 'B' for In-Line
            - 'C' for Pre-Ampli
        if type = 's', return a string :
            - "Booster" for Booster
            - "In-Line" for In-Line
            - "Pre-Amplifier" for Pre-Ampli
        '''
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
            if type.lower() == "c":
                return "A"
            elif type.lower() == "s":
                return "Booster"
            else:
                return 0
        elif re.findall("B", ID.split("/")[2].split("-")[2]) != []:
            if type.lower() == "c":
                return "B"
            elif type.lower() == "s":
                return "In-Line"
            else:
                return 1
        elif re.findall("C", ID.split("/")[2].split("-")[2]) != []:
            if type.lower() == "c":
                return "C"
            elif type.lower() == "s":
                return "Pre-Amplifier"
            else:
                return 2
        else:
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
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Power")
            else:
                return -10 * log(Power/100)
        else:
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


    def GetInVoltage(self):
        '''
        Get input binary voltage of the EFA equipment
        The return voltage is expressed in binary unit (V = 2.048 / 4096)
        '''
        from PyApex.Constantes import SimuEFA_InVoltage
        
        if self.Simulation:
            InVoltage = SimuEFA_InVoltage
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:POWERINVALUE\n"
            Send(self.Connexion, Command)
            InVoltage = Receive(self.Connexion)
        
        return int(InVoltage[:-1])


    def GetOutVoltage(self):
        '''
        Get output binary voltage of the EFA equipment
        The return voltage is expressed in binary unit (V = 2.048 / 4096)
        '''
        from PyApex.Constantes import SimuEFA_OutVoltage
        
        if self.Simulation:
            InVoltage = SimuEFA_OutVoltage
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:POWEROUTVALUE\n"
            Send(self.Connexion, Command)
            InVoltage = Receive(self.Connexion)
        
        return int(InVoltage[:-1])


    def SetIPump(self, IPump):
        '''
        Set laser pump current of the EFA equipment
        IPump is expressed in mA
        '''
        from PyApex.Constantes import APXXXX_ERROR__ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyAPex.Constantes import AP1000_EFA_IPMAX
        from PyApex.Errors import ApexError
        
        try:
            IPump = float(IPump)
        except:
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR__ARGUMENT_TYPE, "IPump")
        else:
            if IPump > AP1000_EFA_IPMAX[self.Type]:
                IPump = AP1000_EFA_IPMAX[self.Type]
            if IPump < 0:
                IPump = 0
            
            if not self.Simulation:
                Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:PUMP" + \
                          ("%.1f" % IPump) + "\n"
                Send(self.Connexion, Command)
            
            self.IPump = IPump


    def GetInPower(self):
        '''
        Get input power of the EFA equipment
        The return power is expressed in the unit defined by the GetUnit() method
        '''
        from PyApex.Constantes import SimuEFA_InPower
        
        if self.Simulation:
            Power = SimuEFA_InPower
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:INDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return float(Power[:-1])


    def GetOutPower(self):
        '''
        Get output power of the EFA equipment
        The return power is expressed in the unit defined by the GetUnit() method
        '''
        from PyApex.Constantes import SimuEFA_OutPower
        
        if self.Simulation:
            Power = SimuEFA_OutPower
        else:
            Command = "AMP[" + str(self.SlotNumber).zfill(2) + "]:OTDB?\n"
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return float(Power[:-1])


    def SetUnit(self, Unit):
        '''
        Set the power unit of the EFA equipment
        Unit is a string which could be "dBm" for logaritmic or "mW" for linear power
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
        Get power unit of the EFA equipment
        The return unit is a string
        '''
        return self.Unit
