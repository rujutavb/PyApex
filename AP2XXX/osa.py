from PyApex.Common import Send, Receive
import sys


class OSA():


    def __init__(self, Equipment, Simulation=False):
        '''
        Constructor of a Heterodyne OSA equipment.
        Equipment is the AP2XXX class of the equipment
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.ID = Equipment.GetID()
        self.Type = self.GetType()
        
        # Variables and constants of the equipment
        self.StartWavelength = AP2XXX_WLMIN
        self.StopWavelength = AP2XXX_WLMAX
        self.Span = AP2XXX_WLMAX - AP2XXX_WLMIN
        self.Center = AP2XXX_WLMIN + (self.Span / 2)
        self.SweepResolution = 1.12 
        self.ValidSweepResolutions = [0 , 1 , 2]
        self.NoiseMaskValue = -70
        self.ValidScaleUnits = [0 , 1]
        self.ScaleXUnit = 1
        self.ScaleYUnit = 1
        self.ValidPolarizationModes = [0 , 1 , 2 , 3]
        self.PolarizationMode = 0
        self.Validtracenumbers = [0 , 1 , 2 , 3 , 4 , 5 , 6]
        self.tracenumber = 1
        self.NAverageOSA = 5


    def __str__(self):
        '''
        Return the equipment type and the AP2XXX ID
        '''
        return "Heterodyne OSA " + str(self.ID)
    
    
    def GetType(self):
        '''
        Return the type of the OSA. For example "AP2061" for an AP2061
        '''
        from PyApex.Errors import ApexError
        import re
        
        Type = self.ID.split("/")[1]
        Type = "AP" + Type
        return Type
        
        
    def SetStartWavelength(self, Wavelength):
        '''
        Set the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_WLMIN, AP2XXX_WLMAX        
        from PyApex.Errors import ApexError
        
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if Wavelength < AP2XXX_WLMIN or Wavelength > AP2XXX_WLMAX:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()

        if not self.Simulation:
            Command = "SPSTRTWL" + str(Wavelength) + "\n"
            Send(self.Connexion, Command)

        self.StartWavelength = Wavelength
        self.Span = self.StopWavelength - self.StartWavelength
        self.Center = self.StartWavelength + (self.Span / 2)


    def GetStartWavelength(self):
        '''
        Get the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import SimuAP2XXX_StartWavelength
        
        if self.Simulation:
            Wavelength = SimuAP2XXX_StartWavelength
        else:
            Command = "SPSTRTWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)

        return float(Wavelength[:-1])


    def SetStopWavelength(self, Wavelength):
        '''
        Set the stop wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_WLMIN, AP2XXX_WLMAX        
        from PyApex.Errors import ApexError
        
        if not isinstance(Wavelength, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Wavelength")
            sys.exit()
        if Wavelength < AP2XXX_WLMIN or Wavelength > AP2XXX_WLMAX:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Wavelength")
            sys.exit()

        if not self.Simulation:
            Command = "SPSTOPWL" + str(Wavelength) + "\n"
            Send(self.Connexion, Command)

        self.StopWavelength = Wavelength
        self.Span = self.StopWavelength - self.StartWavelength
        self.Center = self.StartWavelength + (self.Span / 2)


    def GetStopWavelength(self):
        '''
        Get the stop wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        from PyApex.Constantes import SimuAP2XXX_StopWavelength
        
        if self.Simulation:
            Wavelength = SimuAP2XXX_StopWavelength
        else:
            Command = "SPSTOPWL?\n"
            Send(self.Connexion, Command)
            Wavelength = Receive(self.Connexion)

        return float(Wavelength[:-1])

        
    def SetSpan(self, Span):
        '''
        Set the wavelength measurement span
        Span is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_MINSPAN, AP2XXX_MAXSPAN   
        from PyApex.Errors import ApexError
        
        if not isinstance(Span, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Span")
            sys.exit()
        if Span < AP2XXX_MINSPAN or Span > AP2XXX_MAXSPAN:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Span")
            sys.exit()

        if not self.Simulation:
            Command = "SPSPANWL" + str(Span) + "\n"
            Send(self.Connexion, Command)

        self.StopWavelength
        self.Span = Span
        self.StopWavelength = self.Center + (self.Span / 2)
        self.StartWavelength = self.Center - (self.Span / 2)

        
    def GetSpan(self):
        '''
        Get the wavelength measurement span
        Span is expressed in nm
        '''
        from PyApex.Constantes import SimuAP2XXX_Span
        
        if self.Simulation:
            Span = SimuAP2XXX_Span
        else:
            Command = "SPSPANWL?\n"
            Send(self.Connexion, Command)
            Span = Receive(self.Connexion)

        return float(Span[:-1])

        
    def SetCenter(self, Center):
        '''
        Set the wavelength measurement center
        Center is expressed in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_MINCENTER, AP2XXX_MAXCENTER 
        from PyApex.Errors import ApexError
        
        if not isinstance(Center, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Center")
            sys.exit()
        if Center < AP2XXX_MINCENTER or Center > AP2XXX_MAXCENTER:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Center")
            sys.exit()

        if not self.Simulation:
            Command = "SPCTRWL" + str(Center) + "\n"
            Send(self.Connexion, Command)

        self.Center = Center
        self.StopWavelength = self.Center + (self.Span / 2)
        self.StartWavelength = self.Center - (self.Span / 2)

        
    def GetCenter(self):
        '''
        Get the wavelength measurement center
        Center is expressed in nm
        '''
        from PyApex.Constantes import SimuAP2XXX_Center
        
        if self.Simulation:
            Center = SimuAP2XXX_Center
        else:
            Command = "SPCTRWL?\n"
            Send(self.Connexion, Command)
            Center = Receive(self.Connexion)

        return float(Center[:-1])

        
    def SetXResolution(self, Resolution):
        '''
        Set the wavelength measurement resolution
        Resolution is expressed in the value of 'ScaleXUnit'
        '''
        if not self.Simulation:
            Command = "SPSWPRES" + str(Resolution) + "\n"
            Send(self.Connexion, Command)

            
    def GetXResolution(self):
        '''
        Get the wavelength measurement resolution
        Resolution is expressed in the value of 'ScaleXUnit'
        '''
        from PyApex.Constantes import SimuAP2XXX_XResolution
        
        if self.Simulation:
            Resolution = SimuAP2XXX_XResolution
        else:
            Command = "SPSWPRES?\n"
            Send(self.Connexion, Command)
            Resolution = Receive(self.Connexion)

        return float(Resolution[:-1])

        
    def SetYResolution(self, Resolution):
        '''
        Set the Y-axis power per division value
        Resolution is expressed in the value of 'ScaleYUnit'
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_MINYRES, AP2XXX_MAXYRES
        from PyApex.Errors import ApexError
        
        if not isinstance(Resolution, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Resolution")
            sys.exit()
        if Resolution < AP2XXX_MINYRES or Resolution > AP2XXX_MAXYRES:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Resolution")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPDIVY" + str(Resolution) + "\n"
            Send(self.Connexion, Command)

            
    def GetYResolution(self):
        '''
        Get the Y-axis power per division value
        Resolution is expressed in the value of 'ScaleYUnit'
        '''
        from PyApex.Constantes import SimuAP2XXX_YResolution
        
        if self.Simulation:
            Resolution = SimuAP2XXX_YResolution
        else:
            Command = "SPDIVY?\n"
            Send(self.Connexion, Command)
            Resolution = Receive(self.Connexion)

        return float(Resolution[:-1])

        
    def SetNPoints(self, NPoints):
        '''
        Set the number of points for the measurement
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_MINNPTS, AP2XXX_MAXNPTS 
        from PyApex.Errors import ApexError
        
        if not isinstance(NPoints, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "NPoints")
            sys.exit()
        if NPoints < AP2XXX_MINNPTS or NPoints > AP2XXX_MAXNPTS:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "NPoints")
            sys.exit()

        if not self.Simulation:
            Command = "SPNBPTSWP" + str(NPoints) + "\n"
            Send(self.Connexion, Command)

            
    def GetNPoints(self):
        '''
        Get the number of points for the measurement
        '''
        from PyApex.Constantes import SimuAP2XXX_NPoints
        
        if self.Simulation:
            NPoints = SimuAP2XXX_NPoints
        else:
            Command = "SPNBPTSWP?\n"
            Send(self.Connexion, Command)
            NPoints = Receive(self.Connexion)

        return int(NPoints[:-1])

        
    def Run(self, Type="single"):
        '''
        Run a measurement.
        If Type is
            - "auto" or 0, an auto-measurement is running
            - "single" or 1, a single measurement is running (default)
            - "repeat" or 2, a repeat measurement is running
        '''
        if not self.Simulation:
            if isinstance(Type, str):
                if Type.lower() == "auto":
                    Command = "SPSWP0\n"                    
                elif Type.lower() == "repeat":
                    Command = "SPSWP2\n"
                else:
                    Command = "SPSWP1\n"
            else:
                if Type == 0:
                    Command = "SPSWP0\n"
                elif Type == 2:
                    Command = "SPSWP2\n"
                else:
                    Command = "SPSWP1\n"
            
            
            Send(self.Connexion, Command)
            try:
                status = int(Receive(self.Connexion))
            except:
                status = 0
        else:
            status = 1
            
        return status

            
    def Stop(self):
        '''
        Stop a measurement
        '''
        if not self.Simulation:
            Command = "SPSWP3\n"
            Send(self.Connexion, Command)


    def GetData(self, Scale="log", TraceNumber=1):
        '''
        Get the spectrum data of a measurement
        returns a 2D list [Y-axis Data, X-Axis Data]
        Scale is a string which can be :
            - "log" : get the Y-Axis Data in dBm (default)
            - "lin" : get the Y-Axis Data in mW
        TraceNumber is an integer between 1 (default) and 6
        '''
        from random import random
        from math import log10
        from PyApex.Constantes import SimuAP2XXX_StartWavelength, SimuAP2XXX_StopWavelength
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE 
        from PyApex.Errors import ApexError
        
        if not isinstance(Scale, str):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Scale")
            sys.exit()
            
        if not isinstance(TraceNumber, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()
        
        NPoints = self.GetNPoints()
        if not self.Simulation:
            YData = []
            XData = []
            
            if Scale.lower() == "lin":
                Command = "SPDATAL" + str(int(TraceNumber)) + "\n"
            else:
                Command = "SPDATAD" + str(int(TraceNumber)) + "\n"
            Send(self.Connexion, Command)
            YStr = Receive(self.Connexion, 12 * NPoints)[:-1]
            YStr = YStr.split(" ")
            for s in YStr:
                try:
                    YData.append(float(s))
                except:
                    YData.append(0.0)
                
            Command = "SPDATAWL" + str(TraceNumber) + "\n"
            Send(self.Connexion, Command)
            XStr = Receive(self.Connexion, 12 * NPoints)[:-1]
            XStr = XStr.split(" ")
            for s in XStr:
                try:
                    XData.append(float(s))
                except:
                    XData.append(0.0)
        else:
            YData = []
            XData = []
            DeltaX = (SimuAP2XXX_StopWavelength - SimuAP2XXX_StartWavelength) / NPoints
            for i in range(0, NPoints):
                if Scale.lower() == "lin":
                    YData.append(random())
                else:
                    YData.append(10 * log10(random()))
                XData.append(SimuAP2XXX_StartWavelength + i * DeltaX)
                
        return [YData[1:], XData[1:]]


    def SetNoiseMask(self, NoiseMaskValue):
        '''
        Set the noise mask of the signal (values under this mask are set to this value)
        Noise mask is expressed in the value of 'ScaleYUnit'
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE 
        from PyApex.Errors import ApexError
        
        if not isinstance(NoiseMaskValue, (float, int)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "NoiseMaskValue")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPSWPMSK" + str(NoiseMaskValue) + "\n"
            Send(self.Connexion, Command)

        self.NoiseMaskValue = NoiseMaskValue


    def SetScaleXUnit(self, ScaleXUnit=0):
        '''
        Defines the unit of the X-Axis
        ScaleXUnit can be a string or an integer
        If ScaleXUnit is :
            - "ghz" or 0, X-Axis unit is in GHz (default)
            - "nm" or 1, X-Axis unit is in nm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if isinstance(ScaleXUnit, str):
            if ScaleXUnit.lower() == "nm":
                ScaleXUnit = 1
            else:
                ScaleXUnit = 0
        
        if not isinstance(ScaleXUnit, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ScaleXUnit")
            sys.exit()

        if not ScaleXUnit in self.ValidScaleUnits:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ScaleXUnit")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPXUNT" + str(ScaleXUnit) + "\n"
            Send(self.Connexion, Command)

        self.ScaleXUnit = ScaleXUnit


    def SetScaleYUnit(self, ScaleYUnit=0):
        '''
        Defines the unit of the Y-Axis
        ScaleXUnit can be a string or an integer
        If ScaleYUnit is :
            - "lin" or 0, Y-Axis unit is in mW (default)
            - "log" or 1, Y-Axis unit is in dBm or dBm
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if isinstance(ScaleYUnit, str):
            if ScaleYUnit.lower() == "log":
                ScaleYUnit = 1
            else:
                ScaleYUnit = 0
        
        if not isinstance(ScaleYUnit, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ScaleYUnit")
            sys.exit()

        if not ScaleYUnit in self.ValidScaleUnits:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "ScaleYUnit")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPLINSC" + str(ScaleYUnit) + "\n"
            Send(self.Connexion, Command)

        self.ScaleYUnit = ScaleYUnit


    def SetPolarizationMode(self, PolarizationMode):
        '''
        Defines the measured polarization channels
        PolarizationMode can be a string or an integer
        If PolarizationMode is :
            - "1+2" or 0, the total power is measured (default)
            - "1&2" or 1, one measure is done for each polarization channel
            - "1" or 2, just the polarization channel 1 is measured
            - "2" or 3, just the polarization channel 2 is measured
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if isinstance(PolarizationMode, str):
            if PolarizationMode.lower() == "1&2":
                PolarizationMode = 1
            elif PolarizationMode.lower() == "1":
                PolarizationMode = 2
            elif PolarizationMode.lower() == "2":
                PolarizationMode = 3
            else:
                PolarizationMode = 0
        
        if not isinstance(PolarizationMode, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "PolarizationMode")
            sys.exit()

        if not PolarizationMode in self.ValidPolarizationModes:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "PolarizationMode")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPPOLAR" + str(PolarizationMode) + "\n"
            Send(self.Connexion, Command)

        self.PolarizationMode = PolarizationMode


    def WavelengthCalib(self):
        '''
        Performs a wavelength calibration.
        If a measurement is running, it is previously stopped
        '''
        if not self.Simulation:
            Command = "SPWLCALM\n"
            Send(self.Connexion, Command)


    def DeleteAll(self):
        '''
        Clear all traces
        '''
        if not self.Simulation:
            Command = "SPTRDELAL\n"
            Send(self.Connexion, Command)


    def ActivateAutoNPoints(self):
        '''
        Activates the automatic number of points for measurements
        '''
        if not self.Simulation:
            Command = "SPAUTONBPT1\n"
            Send(self.Connexion, Command)


    def DeactivateAutoNPoints(self):
        '''
        Deactivates the automatic number of points for measurements
        '''
        if not self.Simulation:
            Command = "SPAUTONBPT0\n"
            Send(self.Connexion, Command)


    def FindPeak(self, TraceNumber=1, ThresholdValue=20.0, Axis='X', Find="max"):
        '''
        Find the peaks in the selected trace
        TraceNumber is an integer between 1 (default) and 6
        ThresholdValue is a float expressed in dB
        Axis is a string or an integer for selecting the axis:
            Axis = 0 or 'X' : get the X-axis values of the markers (default)
            Axis = 1 or 'Y' : get the Y-axis values of the markers
        Find is a string between the following values:
            - Find = "MAX" : only the max peak is returned (default)
            - Find = "MIN" : only the min peak is returned
            - Find = "ALL" : all peaks are returned in a list
            - Find = "MEAN" : a mean value of all peaks is returned
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()
            
        if not Axis in [0, 1] and not str(Axis).lower() in ['x', 'y'] :
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Axis")
            sys.exit()

        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
        
        if not isinstance(ThresholdValue, (int, float)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ThresholdValue")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPPKFIND" + str(TraceNumber) + "_" + str(ThresholdValue) + "\n"
            Send(self.Connexion, Command)
            Peaks = self.GetMarkers(TraceNumber, Axis=Axis)
        
        else:
            Peaks = [1545.000, 1550.000, 1555.000]
            
        if str(Find).lower() == "all":
            return Peaks
        
        elif str(Find).lower() == "mean":
            if len(Peaks) > 0:
                Sum = 0
                for p in Peaks:
                    Sum += p
                return Sum / len(Peaks)
            else:
                return 0.0
        
        elif str(Find).lower() == "min":
            if len(Peaks) > 0:
                Min = Peaks[0]
                for p in Peaks:
                    if Min > p:
                        Min = p
                return Min
            else:
                return 0.0
        
        else:
            if len(Peaks) > 0:
                Max = Peaks[0]
                for p in Peaks:
                    if Max < p:
                        Max = p
                return Max
            else:
                return 0.0
        
        self.tracenumber = TraceNumber
        return Peak


    def ActivateAverageMode(self):
        '''
        Activates the average mode
        '''
        if not self.Simulation:
            Command = "SPAVERAGE1\n"
            Send(self.Connexion, Command)


    def DeactivateAverageMode(self):
        '''
        Deactivates the average mode
        '''
        if not self.Simulation:
            Command = "SPAVERAGE0\n"
            Send(self.Connexion, Command)


    def AutoMeasure(self, TraceNumber=1, NbAverage=1):
        '''
        Auto measurement which performs a single and looks for the maximum peak
        If a peak is detected, this method selects the spectral range and modify the span
        TraceNumber is an integer between 1 (default) and 6
        NbAverage is the number of average to perform after the span selection (no average by default)
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Constantes import AP2XXX_WLMIN, AP2XXX_WLMAX
        from PyApex.Errors import ApexError
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()
            
        if not isinstance(NbAverage, (int, float)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "NbAverage")
            sys.exit()
            
        if int(NbAverage) < 1:
            NbAverage = 1

        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
            
        self.DeleteAll()
        self.SetStartWavelength(AP2XXX_WLMIN)
        self.SetStopWavelength(AP2XXX_WLMAX)
        self.Run()
        
        PeakValue = self.FindPeak(TraceNumber, ThresholdValue=20.0, Find="Max")
        
        if PeakValue != 0.0:
            if self.ScaleXUnit == 0:
                self.SetSpan(125.0)
            else:
                self.SetSpan(1.0)
            self.SetCenter(PeakValue)
            
            self.DeleteAll()
            self.DelAllMarkers(TraceNumber)
            
            if int(NbAverage) > 1:
                self.ActivateAverageMode()
            for i in range(NbAverage):
                self.Run()
            if int(NbAverage) > 1:
                self.DesactivateAverageMode()
    
    
    def AddMarker(self, Position, TraceNumber=1):
        '''
        Add a marker
        TraceNumber is an integer between 1 (default) and 6
        Position is the X-axis position of the marker expressed in the value of 'ScaleXUnit'
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()
            
        if not isinstance(Position, (int, float)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Position")
            sys.exit()
        
        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPMKRAD" + str(TraceNumber) + "_" + str(Position) + "\n"
            Send(self.Connexion, Command)
    
    
    def GetMarkers(self, TraceNumber=1, Axis='y'):
        '''
        Gets the X-axis or Y-axis markers of a selected trace
        TraceNumber is an integer between 1 (default) and 6
        Axis is a string or an integer for selecting the axis:
            Axis = 0 or 'X' : get the X-axis values of the markers
            Axis = 1 or 'Y' : get the Y-axis values of the markers (default)
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if not isinstance(Axis, (int, str)):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Axis")
            sys.exit()
        
        if not Axis in [0, 1] and not str(Axis).lower() in ['x', 'y'] :
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "Axis")
            sys.exit()
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()
        
        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
        
        if str(Axis).lower() == 'x':
            Axis = 0
        else:
            Axis = 1
        
        Markers = []
        if not self.Simulation:
            if Axis:
                Command = "SPDATAMKRY" + str(TraceNumber) + "\n"
            else:
                Command = "SPDATAMKRX" + str(TraceNumber) + "\n"
            Send(self.Connexion, Command)
            Str = Receive(self.Connexion, 64)[:-1]
            Str = Str.split(" ")
            Str = Str[1:]
            
            for v in Str:
                if v.lower() not in ["dbm", "mw", "nm", "ghz"]:
                    try:
                        Markers.append(float(v))
                    except:
                        pass
        return Markers
    
    
    def DelAllMarkers(self, TraceNumber=1):
        '''
        Deletes all markers of a selected trace
        TraceNumber is an integer between 1 (default) and 6
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()
        
        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
        
        Markers = []
        if not self.Simulation:
            Command = "SPMKRDELAL" + str(TraceNumber) + "\n"
            Send(self.Connexion, Command)
        

    def LineWidth(self, TraceNumber=1, Get="width"):
        '''
        Gets the 3-db line width of the selected trace
        TraceNumber is an integer between 1 (default) and 6
        ThresholdValue is a float expressed in dB
        Get is a string between the following values:
            - Get = "WIDTH" : only the line width is returned (default)
            - Get = "CENTER" : only the line width center is returned
            - Get = "LEVEL" : only the line width peak level is returned
            - Get = "ALL" : all line width values are returned in a list
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE 
        from PyApex.Errors import ApexError
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()

        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
        
        if not self.Simulation:
            Command = "SPLWTH" + str(TraceNumber) + "_3.0\n"
            Send(self.Connexion, Command)
            Str = Receive(self.Connexion, 64)[:-1]
            Values = []
            Str = Str.split("_")
            
            for s in Str:
                for v in s.split(" "): 
                    if v.lower() not in ["dbm", "mw", "nm", "ghz"]:
                        try:
                            Values.append(float(v))
                        except:
                            pass
            while len(Values) < 3:
                Values.append(0.0)
        
        else:
            Values = [0.100, 1550.000, 2.25]
            
        if str(Get).lower() == "all":
            return Values
        
        elif str(Get).lower() == "center":
            return Values[1]
        
        elif str(Get).lower() == "level":
            return Values[2]
        
        else:
            return Values[0]
    
    
    def SaveToFile(self, FileName, TraceNumber=1, Type="dat"):
        '''
        Save a trace on local hard disk
        FileName is a string representing the path of the file to save
        TraceNumber is an integer between 1 (default) and 6
        Type is the type of the file to save
        Type is a string between the following values:
            - Type = "DAT" : data are saved in a binary format (default)
            - Type = "TXT" : data are saved in a text format
        '''
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE, APXXXX_ERROR_BAD_FILENAME
        from PyApex.Errors import ApexError
        from os.path import isdir, dirname
        
        if not isinstance(TraceNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "TraceNumber")
            sys.exit()

        if not TraceNumber in self.Validtracenumbers:
            raise ApexError(APXXXX_ERROR_ARGUMENT_VALUE, "TraceNumber")
            sys.exit()
        
        if not isdir(dirname(FileName)):
            raise ApexError(APXXXX_ERROR_BAD_FILENAME, str(FileName))
            sys.exit()
        
        if str(Type).lower() == "txt":
            Type = 1
        else:
            Type = 0
        
        if not self.Simulation:
            if Type:
                Command = "SPSAVEB" + str(TraceNumber) + "_" + str(FileName) + "\n"
            else:
                Command = "SPSAVEA" + str(TraceNumber) + "_" + str(FileName) + "\n"
            Send(self.Connexion, Command)