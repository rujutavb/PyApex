

from PyApex.Common import Send, Receive


class PowerMeter1():

    def __init__(self, Equipment, SlotNumber=1, Simulation=False):
        '''
        Constructor of a PW1 (Power Meter1) equipment.
        Equipement is the AP1000 class of the equipement
        SlotNumber is the number of the slot used by the PW1
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        self.__Connexion = Equipment.Connexion
        self.__Simulation = Simulation
        self.__SlotNumber = SlotNumber
        self.__Unit = "dBm"
        self.__Wavelength = 1550
        self.__AvgTime = 100
        self.__Channels = self.GetChannels()
        self.__ValidUnits = ["dbm", "mw"]


    def __str__(self):
        '''
        Return the equipement name and the slot number when the 'print()' function is used
        '''
        return "Optical Power Meter1 in slot " + str(self.__SlotNumber)


    def GetChannels(self):
        '''
        Return the type(s) of the PW1 in a list
        return 1 for a Standard PW1
        return 3 for a High Power PW1
        '''
        from PyApex.Constantes import SimuPW1_SlotID, AP1000_PW1_CHTYPE
        
        if self.__Simulation:
            ID = SimuPW1_SlotID
        else:
            Command = "SLT[" + str(self.__SlotNumber).zfill(2) + "]:IDN?\n"
            Send(self.__Connexion, Command)
            ID = Receive(self.__Connexion)
        
        Channels = []
        for c in ID.split("/")[2].split("-")[3]:
            for k, v in AP1000_PW1_CHTYPE.items():
                if c == k:
                    Channels.append(v)
        
        return Channels


    def SetAverageTime(self, AvgTime):
        '''
        Set the average time of the PW1 equipment
        AvgTime is expressed in ms
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_PW1_AVGMIN, AP1000_PW1_AVGMAX
        from PyApex.Errors import ApexError
        
        try:
            AvgTime = float(AvgTime)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "AvgTime")
        else:
            if AvgTime < AP1000_PW1_AVGMIN:
                print("PyApex Warning. PW1 Average time is set to its minimum value: " + \
                      str(AP1000_PW1_AVGMIN) + " ms !")
                AvgTime = AP1000_PW1_AVGMIN
            if AvgTime > AP1000_PW1_AVGMAX:
                print("PyApex Warning. PW1 Average time is set to its maximum value: " + \
                      str(AP1000_PW1_AVGMAX) + " ms !")
                AvgTime = AP1000_PW1_AVGMAX
            
            if not self.__Simulation:
                Command = "POW1[" + str(self.__SlotNumber).zfill(2) + "]:SETAVERAGE" + \
                          str(AvgTime) + "\n"
                Send(self.__Connexion, Command)
            
            self.__AvgTime = AvgTime


    def GetAverageTime(self):
        '''
        Get the average time of the PW1 equipment
        AvgTime is expressed in ms
        '''
        
        if not self.__Simulation:
            Command = "POW1[" + str(self.__SlotNumber).zfill(2) + "]:GETAVERAGE\n"
            Send(self.__Connexion, Command)
            self.__AvgTime = float(Receive(self.__Connexion)[:-1])
            
        return self.__AvgTime


    def SetUnit(self, Unit):
        '''
        Set the power unit of the PW1 equipment
        Unit is a string which could be "dBm" for logaritmic or "mW" for linear power
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        
        try:
            Unit = str(Unit)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Unit")
        else:
            if Unit.lower() in self.__ValidUnits:
                self.__Unit = Unit


    def GetUnit(self):
        '''
        Get power unit of the PW1 equipment
        The return unit is a string
        '''
        return self.__Unit


    def SetWavelength(self, Wavelength, ChNumber=1):
        '''
        Set wavelength of the channel ChNumber of the PW1 equipment
        Wavelength is expressed in nm
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP1000_PW1_WLMIN, AP1000_PW1_WLMAX
        from PyApex.Errors import ApexError
        
        try:
            Wavelength = float(Wavelength)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
        else:
            try:
                ChNumber = int(ChNumber)
            except:
                self.__Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
            else:
                if Wavelength < AP1000_PW1_WLMIN:
                    print("PyApex Warning. PW1 Wavelength is set to its minimum value: " + \
                          str(AP1000_PW1_WLMIN) + " nm !")
                    Wavelength = AP1000_PW1_WLMIN
                if Wavelength > AP1000_PW1_WLMAX:
                    print("PyApex Warning. PW1 Wavelength is set to its maximum value: " + \
                          str(AP1000_PW1_WLMAX) + " nm !")
                    Wavelength = AP1000_PW1_WLMAX
                if ChNumber > len(self.__Channels):
                    print("PyApex Warning. PW1 Channel is set to 1 !")
                    ChNumber = 1
                
                if not self.__Simulation:
                    Command = "POW1[" + str(self.__SlotNumber).zfill(2) + \
                              "]:SETWAVELENGTH[" + str(ChNumber) + "]" + \
                              ("%4.3f" % Wavelength).zfill(8) + "\n"
                    Send(self.__Connexion, Command)
                
                self.__Wavelength = Wavelength


    def GetWavelength(self, ChNumber=1):
        '''
        Get wavelength of the channel ChNumber of the PW1 equipment
        The return wavelength is expressed in nm
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        
        try:
            ChNumber = int(ChNumber)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        else:
            if ChNumber > len(self.__Channels):
                print("PyApex Warning. PW1 Channel is set to 1 !")
                ChNumber = 1
            
            if not self.__Simulation:
                Command = "POW1[" + str(self.__SlotNumber).zfill(2) + "]:WAV[" + \
                          str(ChNumber) + "]?\n"
                Send(self.__Connexion, Command)
                self.__Wavelength = float(Receive(self.__Connexion)[:-1])
                print(self.__Wavelength)#testing wavelength value that is received 
            return self.__Wavelength


    def SetFrequency(self, Frequency, ChNumber=1):
        '''
        Set frequency of the channel ChNumber of the PW1 equipment
        Frequency is expressed in GHz
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import VACCUM_LIGHT_SPEED, AP1000_PW1_WLMAX
        from PyApex.Errors import ApexError
        
        try:
            Frequency = float(Frequency)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Frequency")
        else:
            try:
                ChNumber = int(ChNumber)
            except:
                self.__Connexion.close()
                raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
            else:
                if ChNumber > len(self.__Channels):
                    print("PyApex Warning. PW1 Channel is set to 1 !")
                    ChNumber = 1
                    
                if Frequency > 0:
                    self.SetWavelength(VACCUM_LIGHT_SPEED / Frequency, ChNumber)
                else:
                    print("PyApex Warning. PW1 Frequency is set to its minimum value: " + \
                          str(AP1000_PW1_WLMAX / VACCUM_LIGHT_SPEED) + " GHz !")
                    self.SetWavelength(AP1000_PW1_WLMAX, ChNumber)


    def GetFrequency(self, ChNumber=1):
        '''
        Set frequency of the channel ChNumber of the PW1 equipment
        Frequency is expressed in GHz
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import VACCUM_LIGHT_SPEED
        from PyApex.Errors import ApexError
        
        try:
            ChNumber = int(ChNumber)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        else:
            if ChNumber > len(self.__Channels):
                print("PyApex Warning. PW1 Channel is set to 1 !")
                ChNumber = 1
            
            Wavelength = self.GetWavelength(ChNumber)
            return float(VACCUM_LIGHT_SPEED / Wavelength)


    def GetPower(self, ChNumber=1):
        '''
        Set frequency of the channel ChNumber of the PW1 equipment
        The return power is expressed in the unit defined by the GetUnit() method
        ChNumber is the channel number : 1 (default) or 2
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import APXXXX_ERROR_VARIABLE_NOT_DEFINED
        from PyApex.Constantes import SimuPW1_Power_dBm, SimuPW1_Power_mW
        from PyApex.Errors import ApexError
        
        try:
            ChNumber = int(ChNumber)
        except:
            self.__Connexion.close()
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ChNumber")
        else:
            if ChNumber > len(self.__Channels):
                print("PyApex Warning. PW1 Channel is set to 1 !")
                ChNumber = 1
            
            if self.__Simulation:
                if self.__Unit.lower() == "dbm":
                    Power = SimuPW1_Power_dBm
                elif self.__Unit.lower() == "mw":
                    Power = SimuPW1_Power_mW
                else:
                    self.__Connexion.close()
                    raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.__Unit")
            else:
                if self.__Unit.lower() == "dbm":
                    Command = "POW1[" + str(self.__SlotNumber).zfill(2) + "]:DBM[" + \
                              str(ChNumber) + "]?\n"
                elif self.__Unit.lower() == "mw":
                    Command = "POW1[" + str(self.__SlotNumber).zfill(2) + "]:MW[" + \
                              str(ChNumber) + "]?\n"
                else:
                    self.__Connexion.close()
                    raise ApexError(APXXXX_ERROR_VARIABLE_NOT_DEFINED, "self.__Unit")
                
                Send(self.__Connexion, Command)
                Power = Receive(self.__Connexion)
            
            return float(Power[:-1])
            
