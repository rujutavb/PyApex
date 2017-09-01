import socket
import os, sys, re

from PyApex.Common import Send, Receive

class AP2XXX():
    '''
    DESCRIPTION
        Elementary functions to communicate with Apex AP2XXX equipment (OSA and OCSA)
        This class can control :
            - The heterodyne OSA
            - The polarimeter
            - The optical filter
        This class cannot yet control :
            - The filters OSA (AP207X)
            - The powermeter
            - The tunable laser
        
    VERSION
        2.0
    
    CONTRIBUTORS
        Maxime FONTAINE
        Khalil KECHAOU
    '''

    def __init__(self, IPaddress, PortNumber=5900, Simulation=False):
        '''
        Constructor of AP2XXX equipment.
        IPaddress is the IP address (string) of the equipment.
        PortNumber is by default 5900. It's an integer
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        from PyApex.Constantes import AP2XXX_WLMIN, AP2XXX_WLMAX 
        
        self.IPAddress = IPaddress
        self.PortNumber = PortNumber
        self.Simulation = Simulation
        
        # Connexion to the equipment
        self.Open()
        

    def Open(self):
        '''
        Open connexion to AP2XXX equipment.
        This method is called by the constructor of AP2XXX class
        '''
        self.Connexion = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.Connexion.settimeout(10)
        self.Connexion.setblocking(True)
        
        if self.Simulation:
            print("Connected successfully to the equipment")
        else:
            try:
                self.Connexion.connect((self.IPAddress, self.PortNumber))
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
        
        if not self.Simulation:
            try:
                self.Connexion.close()
            except:
                raise ApexError(APXXXX_ERROR_COMMUNICATION, self.Connexion.getsockname()[0])
                sys.exit()


    def GetID(self):
        '''
        Return string ID of AP2XXX equipment
        '''
        from PyApex.Constantes import SimuAP2XXX_ID
        
        if self.Simulation:
            return SimuAP2XXX_ID
        else:
            Send(self.Connexion, "*IDN?\n")
            ID = Receive(self.Connexion)
            return ID

    
    def OSA(self):
        '''
        Return an OSA object for using the Heterodyne AP2XXX OSA
        '''
        from PyApex.AP2XXX.osa import OSA
        return OSA(self, self.Simulation)
        
        
    def Powermeter(self):
        '''
        Return a Powermeter object for using the embedded powermeter of the AP2XXX
        '''
        from PyApex.AP2XXX.powermeter import Powermeter
        return Powermeter(self, self.Simulation)
        
        
    def OsaFs(self):
        '''
        Return an OSA Fast-Sweep object for using the OSA Fast Sweep of the AP207X
        Only available with the AP207X equipment
        '''
        from PyApex.AP2XXX.osafs import OsaFs
        return OsaFs(self, self.Simulation)
        
        
    def Polarimeter(self):
        '''
        Return a Polarimeter object for using the embedded polarimeter of the AP2XXX
        Available only with the option OSA-12
        '''
        from PyApex.AP2XXX.polarimeter import Polarimeter
        return Polarimeter(self, self.Simulation)
        
        
    def Filter(self):
        '''
        Return a Filter object for using the embedded optical filter of the AP2XXX
        Available only with the option OSA-12
        '''
        from PyApex.AP2XXX.filter import Filter
        return Filter(self, self.Simulation)
    
    
    
        
        
        
        