from PyApex.Common import Send, Receive
import sys


class Powermeter():

    
    def __init__(self, Equipment, Simulation=False):
        '''
        Constructor of a Powermeter embedded in an AP2XXX equipment.
        Equipment is the AP2XXX class of the equipment
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.ID = Equipment.GetID()
        
        # Variables and constants of the equipment
        self.Unit = "dBm"
        self.ValidUnits = ["dbm", "mw"]


    def __str__(self):
        '''
        Return the equipment type and the AP2XXX ID
        '''
        return "Powermeter of " + str(self.ID)
    
    
    def SetUnit(self, Unit):
        '''
        Set the power unit of the Powermeter equipment
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
        Get power unit of the Powermeter equipment
        The return unit is a string
        '''
        return self.Unit
    
    
    def GetPower(self, Polar=0):
        '''
        Get the power measured by the Powermeter equipment
        The return power is expressed in the unit defined by the GetUnit() method
        Polar is the polarization channel :
            - 0 : Total power (default)
            - 1 : Power of polarization channel n°1
            - 2 : Power of polarization channel n°2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Errors import ApexError
        from random import random
        
        if not isinstance(Polar, (int)):
            self.Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Polar")

        if self.Simulation:
            if self.Unit.lower() == "dbm":
                Power = 60.0 * random() - 50.0
            elif self.Unit.lower() == "mw":
                Power = 10.0 * random()
            else:
                self.Connexion.close()
                raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.Unit")
        else:
            Command = "SPMEASDETECTORDBM1\n"               
            Send(self.Connexion, Command)
            Power = Receive(self.Connexion)
        
        return float(Power[:-1])
    
    
    
    
    
    
    
    
    