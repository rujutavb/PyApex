import socket
import os, sys, re

from PyApex.Constantes import *
from PyApex.Errors import ApexError
from PyApex.Common import Send, Receive

class AP2050():

    def __init__(self, IPaddress, PortNumber=5900, Simulation=False):
        self.IPAddress = IPaddress
        self.PortNumber = PortNumber
        self.Simulation = Simulation
        self.Open()
        self.StartWavelength = AP2050_WLMIN
        self.StopWavelength = AP2050_WLMAX
        self.Span = AP2050_WLMAX - AP2050_WLMIN
        self.Center = AP2050_MIN + (self.Span / 2)
        

    def Open(self):
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
        if not self.Simulation:
            try:
                self.Connexion.close()
            except:
                raise ApexError(AP1000_ERROR_COMMUNICATION, self.Connexion.getsockname()[0])
                sys.exit()


    def GetID(self):
        if self.Simulation:
            return SimuAP2050_ID
        else:
            Send(self.Connexion, "*IDN?\n")
            ID = Receive(self.Connexion)
            return ID

      
    def SetStartWavelength(self, Wavelength):
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if Wavelength < AP2050_WLMIN or Wavelength > AP2050_WLMAX:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()

        if not self.Simulation:
            Command = "SPSTRTWL" + str(Wavelength) + "\n"
            Send(self.Connexion, Command)

        self.StartWavelength = Wavelength
        self.Span = self.StopWavelength - self.StartWavelength
        self.Center = self.StartWavelength + (self.Span / 2)


    def GetStartWavelength(self):
        if self.Simulation:
            Wavelength = SimuAP2050_StartWavelength
        else:
            Command = "SPSTRTWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)

        return float(Wavelength[:-1])


    def SetStopWavelength(self, Wavelength):
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if Wavelength < AP2050_WLMIN or Wavelength > AP2050_WLMAX:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()

        if not self.Simulation:
            Command = "SPSTOPWL" + str(Wavelength) + "\n"
            Send(self.Connexion, Command)

        self.StopWavelength = Wavelength
        self.Span = self.StopWavelength - self.StartWavelength
        self.Center = self.StartWavelength + (self.Span / 2)


    def GetStopWavelength(self):
        if self.Simulation:
            Wavelength = SimuAP2050_StartWavelength
        else:
            Command = "SPSTOPWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)

        return float(Wavelength[:-1])

    def SetSpan(self, Span):
        if not isinstance(Span, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Span")
            sys.exit()
        if Span < AP2050_MINSPAN or Span > AP2050_MAXSPAN:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Span")
            sys.exit()

        if not self.Simulation:
            Command = "SPSPANWL" + str(Span) + "\n"
            Send(self.Connexion, Command)

        self.StopWavelength = Wavelength
        self.Span = self.StopWavelength - self.StartWavelength
        self.Center = self.StartWavelength + (self.Span / 2)
