#! /usr/bin/python3
# -*- coding: <utf-8> -*-

import usb.core

'''
struct AB3510_EmbeddedData
{
	// Board general data
	std::string Name;
	std::string FirmwareVersion;
	std::string HardwareVersion;
	std::string SerialNumber;
	std::string PartNumber;

	// Calibration data
	Calibration Channels[4];
};
'''

class AB3510():
    '''
    DESCRIPTION
        Elementary functions to communicate with Apex AB3510 board
        this version can :
            - Get a sample from the four channels
            - Get the temperature value
        this version cannot :
            - Get samples in streaming mode
    VERSION
        1.0
    '''

    def __init__(self, Simulation=False):
        '''
        Constructor of AB3510 equipment.
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        from PyApex.Constantes import ABXXXX_NO_EQUIPMENT_FOUND
        from PyApex.Errors import ApexError
        from sys import exit
        
        self.Simulation = Simulation
        self.Handle = 0
        self.Device = None
        self.Channels = []
        for i in range(0, 4):
            PowerCalib = []
            for k in range(0, 2**14):
                PowerCalib.append(0.0)
            self.Channels.append([PowerCalib, [1.0, 0.0], [1.0, 0.0]])
        
        Devices = self.Find()
        if len(Devices) == 0:
            raise ApexError(ABXXXX_NO_EQUIPMENT_FOUND, "AB3510")
            exit()
        if len(Devices) == 1: 
            self.Open()
        

    def Find(self):
        from PyApex.Constantes import AB3510_VID, AB3510_PID
        Devices = []
        if not self.Simulation:
            for dev in usb.core.find(find_all = True, idVendor = AB3510_VID, idProduct = AB3510_PID):
                Devices.append(dev)
        else:
            Devices.append("AB3510 USB Simulator Device")
        return Devices


    def Open(self, Handle=0):
        '''
        Opens a connexion with an AB3510 equipment.
        This method is called by the constructor of AB3510 class if only 1 board is present
        '''
        from PyApex.Constantes import ABXXXX_ERROR_BAD_HANDLE
        from PyApex.Errors import ApexError
        from sys import exit         
        
        if self.Simulation:
            print("Connected successfully to the equipment")
        else:
            try:
                Devices = self.Find()
                if len(Devices) == 0:
                    raise ApexError(ABXXXX_NO_EQUIPMENT_FOUND, "AB3510")
                    exit()
                elif len(Devices) <= Handle:
                    raise ApexError(ABXXXX_ERROR_BAD_HANDLE, Handle)
                    exit()
                
                self.Device = Devices[Handle]
                self.Device.set_configuration()
                print("Connected successfully to the equipment")
            except:
                print("Cannot connect to the equipment")


    def Close(self):
        '''
        Close connexion with AB3510 equipment
        '''
        self.Device = None


    def GetID(self):
        '''
        Return values of VID and PID of AB3510 equipment
        '''
        from PyApex.Constantes import SIMU_AB3510_VID, SIMU_AB3510_PID
        
        if self.Simulation:
            return [SIMU_AB3510_VID, SIMU_AB3510_PID]
        else:
            return [self.Device.idVendor, self.Device.idProduct]


    def Reset(self):
        '''
        Reset AB3510 equipment
        '''
        from PyApex.Constantes import AB3510_VR_RESET_ALL, ABXXXX_EP0_WRITE_ERROR
        from PyApex.Errors import ApexError
        from sys import exit
        
        if not self.Simulation:
            try:
                self.Device.ctrl_transfer(0x40, AB3510_VR_RESET_ALL, 0, 0)
            except:
                raise ApexError(ABXXXX_EP0_WRITE_ERROR, AB3510_VR_RESET_ALL)
                exit()


    def GetTemperature(self):
        '''
        Get the temperature on AB3510 equipment in degree Celsius
        '''
        from PyApex.Constantes import AB3510_VR_GET_TEMPERATURE, ABXXXX_EP0_READ_ERROR, SIMU_AB3510_TEMPERATURE
        from PyApex.Errors import ApexError
        from random import randint
        from sys import exit

        if self.Simulation:
            return SIMU_AB3510_TEMPERATURE
        else:
            try:
                TempWord = self.Device.ctrl_transfer(0xC0, AB3510_VR_GET_TEMPERATURE, 0, 0, 2)
            except:
                raise ApexError(ABXXXX_EP0_READ_ERROR, AB3510_VR_GET_TEMPERATURE)
                exit()
            else:
                return ((TempWord[0] * 256 + TempWord[1]) / 16) * 0.0625


    def GetSample(self):
        '''
        Get one sample from the 4 channels of AB3510
        '''
        from PyApex.Constantes import AB3510_VR_GET_SAMPLE, ABXXXX_EP0_READ_ERROR
        from PyApex.Errors import ApexError
        from sys import exit

        Samples = []
        if self.Simulation:
            for i in range(0, 4):
                Samples.append(randint(0, 16383))
        else:
            try:
                SampleWord = self.Device.ctrl_transfer(0xC0, AB3510_VR_GET_SAMPLE, 0, 0, 8)
            except:
                raise ApexError(ABXXXX_EP0_READ_ERROR, AB3510_VR_GET_SAMPLE)
                exit()
            else:
                for i in range(0, 8, 2):
                    Samples.append(int((SampleWord[i] + (SampleWord[i + 1] * 256)) / 4))
        return Samples    


    def SetEEPROMParameters(self, Data):
        '''
        Set Parameters into the EEPROM of AB3510
        '''
        from PyApex.Constantes import AB3510_VR_SET_EEPROM_PARAMETERS, ABXXXX_EP0_WRITE_ERROR,\
             APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        from sys import exit

        if not isinstance(Data, bytes):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "Data")
            exit()
        
        if self.Simulation:
            return True
        else:
            self.Device.ctrl_transfer(0x40, AB3510_VR_SET_EEPROM_PARAMETERS, len(Data), 0, Data)
            try:
                len(Data)
            except:
                raise ApexError(ABXXXX_EP0_WRITE_ERROR, AB3510_VR_SET_EEPROM_PARAMETERS)
                return False
            else:
                return True


    def GetEEPROMParameters(self, BytesNumber):
        '''
        Get Parameters from the EEPROM of AB3510
        '''
        from PyApex.Constantes import AB3510_VR_GET_EEPROM_PARAMETERS, ABXXXX_EP0_READ_ERROR,\
             APXXXX_ERROR_ARGUMENT_TYPE
        from PyApex.Errors import ApexError
        from sys import exit

        if not isinstance(BytesNumber, int):
            raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "BytesNumber")
            exit()
        
        if self.Simulation:
            return -1
        else:
            Data = self.Device.ctrl_transfer(0xC0, AB3510_VR_GET_EEPROM_PARAMETERS, BytesNumber, 0, BytesNumber)
            try:
                len(Data)
            except:
                raise ApexError(ABXXXX_EP0_READ_ERROR, AB3510_VR_GET_EEPROM_PARAMETERS)
                return -1
            else:
                return Data



