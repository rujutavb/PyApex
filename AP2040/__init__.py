import socket
import os, sys, re

from PyApex.Constantes import *
from PyApex.Errors import ApexError
from PyApex.Common import Send, Receive

class AP2040():

    def __init__(self, IPaddress, PortNumber=5900, Simulation=False):
        self.IPAddress = IPaddress
        self.PortNumber = PortNumber
        self.Simulation = Simulation
        self.Open()
        self.StartWavelength = AP2040_WLMIN
        self.StopWavelength = AP2040_WLMAX
        self.Span = AP2040_WLMAX - AP2040_WLMIN
        self.Center = AP2040_WLMIN + (self.Span / 2)
        

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
            return SimuAP2040_ID
        else:
            Send(self.Connexion, "*IDN?\n")
            ID = Receive(self.Connexion)
            return ID

      
    def SetStartWavelength(self, Wavelength):
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if Wavelength < AP2040_WLMIN or Wavelength > AP2040_WLMAX:
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
        if Wavelength < AP2040_WLMIN or Wavelength > AP2040_WLMAX:
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
        if Span < AP2040_MINSPAN or Span > AP2040_MAXSPAN:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Span")
            sys.exit()

        if not self.Simulation:
            Command = "SPSPANWL" + str(Span) + "\n"
            Send(self.Connexion, Command)

        self.StopWavelength = Wavelength
        self.Span = self.StopWavelength - self.StartWavelength
        self.Center = self.StartWavelength + (self.Span / 2)

    def GetSpan(self):
        if self.Simulation:
            Span = SimuAP2050_Span
        else:
            Command = "SPSPANWL?\n"
            Send(self.Connexion, Command)
            Span = Receive(self.Connexion)

        return float(Span[:-1])

    def SetCenter(self, Center):
        if not isinstance(Center, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Center")
            sys.exit()
        if Span < AP2040_MINCENTER or Span > AP2040_MAXCENTER:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Center")
            sys.exit()

        if not self.Simulation:
            Command = "SPCTRWL" + str(Center) + "\n"
            Send(self.Connexion, Command)

        self.Center = Center

    def GetCenter(self):
        if self.Simulation:
            Center = SimuAP2050_Center
        else:
            Command = "SPCTRWL?\n"
            Send(self.Connexion, Command)
            Center = Receive(self.Connexion)

        return float(Center[:-1])

    def SetXResolution(self, Resolution):
        if not self.Simulation:
            Command = "SPSWPRES" + str(Resolution) + "\n"
            Send(self.Connexion, Command)

    def GetXResolution(self):
        if self.Simulation:
            Resolution = SimuAP2050_XResolution
        else:
            Command = "SPSWPRES?\n"
            Send(self.Connexion, Command)
            Resolution = Receive(self.Connexion)

        return float(Resolution[:-1])

    def SetYResolution(self, Resolution):
        if not isinstance(Resolution, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Resolution")
            sys.exit()
        if Resolution < AP2040_MINYRES or Resolution > AP2040_MAXYRES:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Resolution")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPDIVY" + str(Resolution) + "\n"
            Send(self.Connexion, Command)

    def GetYResolution(self):
        if self.Simulation:
            Resolution = SimuAP2050_YResolution
        else:
            Command = "SPDIVY?\n"
            Send(self.Connexion, Command)
            Resolution = Receive(self.Connexion)

        return float(Resolution[:-1])

    def SetNPoints(self, NPoints):
        if not isinstance(NPoints, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "NPoints")
            sys.exit()
        if NPoints < AP2040_MINNPTS or NPoints > AP2040_MAXNPTS:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "NPoints")
            sys.exit()

        if not self.Simulation:
            Command = "SPNBPTSWP" + str(NPoints) + "\n"
            Send(self.Connexion, Command)

    def GetNPoints(self):
        if self.Simulation:
            NPoints = SimuAP2050_NPoints
        else:
            Command = "SPNBPTSWP?\n"
            Send(self.Connexion, Command)
            NPoints = Receive(self.Connexion)

        return int(NPoints[:-1])

    def Run(self, Type="Auto"):
        if not self.Simulation:
            if Type.lower() == "auto":
                Command = "SPSWP0\n"
            if Type.lower() == "single":
                Command = "SPSWP1\n"
            if Type.lower() == "repeat":
                Command = "SPSWP2\n"
            Send(self.Connexion, Command)

    def Stop(self):
        if not self.Simulation:
            Command = "SPSWP3\n"
            Send(self.Connexion, Command)

    def GetData(self, Scale="Log", TraceNumber=1):
        if not self.Simulation:
            NPoints = self.GetNPoints()
            Command = "SPDATAD" + str(TraceNumber) + "\n"
            Send(self.Connexion, Command)
            YData = Receive(self.Connexion, NPoints)

            Command = "SPDATAWL" + str(TraceNumber) + "\n"
            Send(self.Connexion, Command)
            XData = Receive(self.Connexion, NPoints)

        return [YData, XData]
