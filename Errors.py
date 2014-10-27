from PyApex.Constantes import *

class ApexError(Exception):

    def __init__(self, ErrorCode=0, ErrorCause=None):
        Exception.__init__(self)
        self.ErrorCause = ErrorCause
        self.ErrorCode = ErrorCode
    
    
    def __str__(self):
        ErrorMsg = "\nPyApex Error " +  str(self.ErrorCode) + " : "
        if self.ErrorCode == AP1000_ERROR_COMMUNICATION:
            ErrorMsg += "Communication with equipment " + str(self.ErrorCause) + " cannot be established"
        elif self.ErrorCode == AP1000_ERROR_BADCOMMAND:
            ErrorMsg += "Command '" + str(self.ErrorCause) + "' can't be interpreted by the equipment"
        elif self.ErrorCode == AP1000_ERROR_ARGUMENT_TYPE:
            ErrorMsg += "Wrong argument type for '" + str(self.ErrorCause) + "'"
        elif self.ErrorCode == AP1000_ERROR_ARGUMENT_VALUE:
            ErrorMsg += "Wrong argument value for '" + str(self.ErrorCause) + "'"
        elif self.ErrorCode == AP1000_ERROR_SLOT_NOT_DEFINED:
            ErrorMsg += "Slot n° " + str(self.ErrorCause) + " has not a defined type"
        elif self.ErrorCode == AP1000_ERROR_SLOT_NOT_GOOD_TYPE:
            ErrorMsg += "Slot n° " + str(self.ErrorCause) + " has not the good type"
        elif self.ErrorCode == AP1000_ERROR_SLOT_TYPE_NOT_DEFINED:
            ErrorMsg += "Slot n° " + str(self.ErrorCause) + " has not the good type"
        elif self.ErrorCode == AP1000_ERROR_VARIABLE_NOT_DEFINED:
            ErrorMsg += "Internal variable '" + str(self.ErrorCause) + "' is not defined"
        else:
            ErrorMsg += "Error code not defined"
        
        return ErrorMsg
