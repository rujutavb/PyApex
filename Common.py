import os, sys

from PyApex.Constantes import *
from PyApex.Errors import ApexError


def Send(Connexion, Command):
    if not isinstance(Command, str):
        raise ApexError(AP1000_ERROR_ARGUMENT_TYPE, "Command")
        sys.exit()
    try:
        Connexion.send(Command.encode('utf-8'))
    except:
        raise ApexError(APXXXX_ERROR_BADCOMMAND, Command)
        sys.exit()


def Receive(Connexion, ByteNumber=1024):
    if not isinstance(ByteNumber, int):
        raise ApexError(APXXXX_ERROR_ARGUMENT_TYPE, "ByteNumber")
        sys.exit()
    try:
        data = Connexion.recv(ByteNumber)
    except:
        raise ApexError(APXXXX_ERROR_COMMUNICATION, Connexion.getsockname()[0])
        sys.exit()
    else:
        return data.decode('utf-8')
