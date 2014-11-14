from PyApex.Common import Send, Receive


class OpticalSwitch():

    def __init__(self, Equipment, SlotNumber=1, Simulation=False):
        self.Connexion = Equipment.Connexion
        self.Simulation = Simulation
        self.SlotNumber = SlotNumber
        self.Path = 0
        
       
    def __str__(self):
        return "Optical Switch in slot " + str(self.SlotNumber)
    
    
    def SetPath(self, Path):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError

        if type(Path) == str:
            if Path.lower() == "crossed":
                self.Path = 1
            else:
                self.Path = 0
        elif type(Path) == int:
            if Path == 1:
                self.Path = 1
            else:
                self.Path = 0
        elif type(Path) == bool:
            if Path == True:
                self.Path = 1
            else:
                self.Path = 0
            
        if not self.Simulation:
            Command = "SWI[" + str(self.SlotNumber).zfill(2) + "]:CONF" + str(self.Path) + "\n"
            Send(self.Connexion, Command)
    
    
    def GetPath(self):
        from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_ARGUMENT_VALUE
        from PyApex.Errors import ApexError
        
        
        if self.Simulation:
            Path = str(self.Path) + "\n"
        else:
            Command = "SWI[" + str(self.SlotNumber).zfill(2) + "]:CONF?\n"
            Send(self.Connexion, Command)
            Path = Receive(self.Connexion)
        
        return (int(Path[:-1]))
