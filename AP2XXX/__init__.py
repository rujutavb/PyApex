import socket
import os, sys, re

from PyApex.Common import Send, Receive

class AP2XXX():
    '''
    DESCRIPTION
        Elementary functions to communicate with Apex AP2XXX equipment (OSA and OCSA)
        This class can control :
            - The heterodyne OSA
            - The polarimeter (option)
            - The optical filter (option)
            - The filters OSA (option)
            - The powermeter
            - The tunable laser (option)
        
    VERSION
        2.0
    
    CONTRIBUTORS
        Maxime FONTAINE
        Khalil KECHAOU
        Vincent PERNET
    '''

    def __init__(self, IPaddress, PortNumber=5900, Simulation=False):
        '''
        Constructor of AP2XXX equipment.
        IPaddress is the IP address (string) of the equipment.
        PortNumber is by default 5900. It's an integer
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        
        self.__IPAddress = IPaddress
        self.__PortNumber = PortNumber
        self.__Simulation = Simulation
        
        # Connexion to the equipment
        self.Open()
        

    def Open(self):
        '''
        Open connexion to AP2XXX equipment.
        This method is called by the constructor of AP2XXX class
        '''
        self.Connexion = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.Connexion.settimeout(10.0)
        
        if self.__Simulation:
            print("Connected successfully to the equipment")
        else:
            try:
                self.Connexion.connect((self.__IPAddress, self.__PortNumber))
                print("Connected successfully to the equipment")
            except:
                print("Cannot connect to the equipment")
                sys.exit()


    def Close(self):
        '''
        Close connexion to AP2XXX equipment
        '''
        from PyApex.Constantes import APXXXX_ERROR_COMMUNICATION 
        from PyApex.Errors import ApexError
        
        if not self.__Simulation:
            try:
                self.Connexion.close()
            except:
                raise ApexError(APXXXX_ERROR_COMMUNICATION, self.Connexion.getsockname()[0])
                sys.exit()

    
    def SetTimeOut(self, TimeOut):
        '''
        Set the timeout of the Ethernet connection
        TimeOut is expressed in seconds
        In some functions like 'OSA.Run()', the timeout is disabled
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        
        if not isinstance(TimeOut, (int, float)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TimeOut")
        
        self.Connexion.settimeout(TimeOut)
    
    
    def GetTimeOut(self):
        '''
        Get the timeout of the Ethernet connection
        The returned value is expressed in seconds
        '''
        
        TimeOut = self.Connexion.gettimeout()
        return TimeOut
    

    def GetID(self):
        '''
        Return string ID of AP2XXX equipment
        '''
        from PyApex.Constantes import SimuAP2XXX_ID
        
        if self.__Simulation:
            return SimuAP2XXX_ID
        else:
            Send(self.Connexion, "*IDN?\n")
            ID = Receive(self.Connexion)
            return ID
    
    
    def ChangeMode(self, Mode):
        '''
        Changes the screen mode of the AP2XXX equipment (Apex Start, O.S.A., Powermeter,...)
        Mode is an integer representing the index of the mode to dsiplay.
        By convention, the "APEX Start" mode is always 0 index. The index follows the
        list in the Apex menu box.
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE
        
        TimeOut = self.Connexion.gettimeout()
        self.Connexion.settimeout(None)
        
        if not isinstance(Mode, (int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Mode")
        
        if not self.__Simulation:
            Send(self.Connexion, "CHMOD" + str(Mode) + "\n")
        
        self.Connexion.settimeout(TimeOut)
    
    
    def DisplayScreen(self, Display):
        '''
        Displays or not the "Remote" window on the AP2XXX equipment.
        Display is a boolean:
            - True: the window is displayed
            - False: the window is hidden
        '''
        
        if Display == False:
            Display = 0
        else:
            Display = 1
        
        if not self.__Simulation:
            Send(self.Connexion, "REMSCREEN" + str(Display) + "\n")

    
    def OSA(self):
        '''
        Return an OSA object for using the Heterodyne AP2XXX OSA
        '''
        from PyApex.AP2XXX.osa import OSA
        return OSA(self, self.__Simulation)


    def OCSA(self):
        '''
        Return an OCSA object for using the Heterodyne AP2XXX OCSA
        '''
        from PyApex.AP2XXX.ocsa import OCSA
        return OCSA(self, self.__Simulation)


    def TLS(self):
        '''
        Return a TLS object for using the Tunable Laser Source of the AP2XXX
        '''
        from PyApex.AP2XXX.tls import TunableLaser
        return TunableLaser(self, self.__Simulation)
        
        
    def Powermeter(self):
        '''
        Return a Powermeter object for using the embedded powermeter of the AP2XXX
        '''
        from PyApex.AP2XXX.powermeter import Powermeter
        return Powermeter(self, self.__Simulation)
        
        
    def OsaFs(self):
        '''
        Return an OSA Fast-Sweep object for using the OSA Fast Sweep of the AP207X
        Only available with the AP207X equipment
        '''
        from PyApex.AP2XXX.osafs import OsaFs
        return OsaFs(self, self.__Simulation)
        
        
    def Polarimeter(self):
        '''
        Return a Polarimeter object for using the embedded polarimeter of the AP2XXX
        Available only with the option OSA-12
        '''
        from PyApex.AP2XXX.polarimeter import Polarimeter
        return Polarimeter(self, self.__Simulation)
        
        
    def Filter(self):
        '''
        Return a Filter object for using the embedded optical filter of the AP2XXX
        Available only with the option OSA-12
        '''
        from PyApex.AP2XXX.filter import Filter
        return Filter(self, self.__Simulation)
    
    
    
        
        
        
        
