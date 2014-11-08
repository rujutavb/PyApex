
def Send(Connexion, Command):
    from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_BADCOMMAND 
    from PyApex.Errors import ApexError
    from sys import exit
    
    if not isinstance(Command, str):
        Connexion.close()
        raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Command")
        sys.exit()
    try:
        Connexion.send(Command.encode('utf-8'))
    except:
        Connexion.close()
        raise ApexError(APXXXX_ERROR_BADCOMMAND, Command)
        sys.exit()


def Receive(Connexion, ByteNumber=1024):
    from PyApex.Constantes import APXXXX_ERROR_ARGUMENT_TYPE, APXXXX_ERROR_COMMUNICATION 
    from PyApex.Errors import ApexError
    from sys import exit
    
    if not isinstance(ByteNumber, int):
        Connexion.close()
        raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ByteNumber")
        sys.exit()
    try:
        data = Connexion.recv(ByteNumber)
    except:
        Connexion.close()
        raise ApexError(APXXXX_ERROR_COMMUNICATION, Connexion.getsockname()[0])
        sys.exit()
    else:
        return data.decode('utf-8')
