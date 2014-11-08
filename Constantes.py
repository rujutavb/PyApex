#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#                                  UNIVERSAL CONSTANTS
# ------------------------------------------------------------------------------
VACCUM_LIGHT_SPEED = 299792458


# ------------------------------------------------------------------------------
#                                   AP1000 CONSTANTS
# ------------------------------------------------------------------------------

#                       CONSTANTS FOR AP1000 MODULES REFERENCE
# ------------------------------------------------------------------------------
AP1000_PWM = 3314
AP1000_PWM_NAME = "Optical Power Meter"
AP1000_TLS_CBAND = 3350
AP1000_TLS_CBAND_NAME = "C Band Tunable Laser Source"
AP1000_TLS_LBAND = 3352
AP1000_TLS_LBAND_NAME = "L Band Tunable Laser Source"
AP1000_OSW = 3344
AP1000_OSW_NAME = "Optical Switch"
AP1000_ATT = 3364
AP1000_ATT_NAME = "Optical Attenuator"
AP1000_EFA_PREAMP = 3370
AP1000_EFA_PREAMP_NAME = "Erbium Doped Fiber Pre-Amplifier"
AP1000_EFA_BOOST = 3371
AP1000_EFA_BOOST_NAME = "Erbium Doped Fiber Booster Amplifier"
AP1000_EFA_INLINE = 3372
AP1000_EFA_INLINE_NAME = "Erbium Doped Fiber In-Line Amplifier"

Modules = {\
    AP1000_TLS_CBAND : AP1000_TLS_CBAND_NAME, \
    AP1000_TLS_LBAND : AP1000_TLS_LBAND_NAME, \
    AP1000_PWM : AP1000_PWM_NAME, \
    AP1000_ATT : AP1000_ATT_NAME, \
    AP1000_EFA_PREAMP : AP1000_EFA_PREAMP_NAME, \
    AP1000_EFA_BOOST : AP1000_EFA_BOOST_NAME, \
    AP1000_EFA_INLINE : AP1000_EFA_INLINE_NAME, \
    AP1000_OSW : AP1000_OSW_NAME,\
}

#                           SLOTS NUMBER MIN AND MAX
# ------------------------------------------------------------------------------
AP1000_SLOT_MIN = 0
AP1000_SLOT_MAX = 92

#                            POWER METER CONSTANTS
# ------------------------------------------------------------------------------
# POWER METER TYPE
AP1000_PWM_CHTYPE = {"1" : "Standard", "3" : "High Power"}
# MIN AND MAX WAVELENGTH
AP1000_PWM_WLMIN = 800
AP1000_PWM_WLMAX = 1700
# MIN AND MAX AVERAGE TIME
AP1000_PWM_AVGMIN = 15
AP1000_PWM_AVGMAX = 10000

#                            ATTENUATOR CONSTANTS
# ------------------------------------------------------------------------------
# NUMBER OF CHANNELS
AP1000_ATT_CHNUMBER = 2
# MIN AND MAX ATTENUATION
AP1000_ATT_ATTMIN = 0
AP1000_ATT_ATTMAX = 31
# MIN AND MAX WAVELENGTH
AP1000_ATT_WLMIN = 1300
AP1000_ATT_WLMAX = 1700

#                           TUNABLE LASER CONSTANTS
# ------------------------------------------------------------------------------
# [3350 : C-BAND TYPE, NOT USED, 3352 : L-BAND TYPE]
# MIN AND MAX POWER
AP1000_TLS_POWMIN = [-30, None, -30]
AP1000_TLS_POWMAX = [13, None, 13]
# MIN AND MAX WAVELENGTH
AP1000_TLS_WLMIN = [1526, None, 1567]
AP1000_TLS_WLMAX = [1567, None, 1608]
# MIN AND MAX FREQUENCY
AP1000_TLS_FRMIN = [VACCUM_LIGHT_SPEED / AP1000_TLS_WLMIN[0], None, VACCUM_LIGHT_SPEED / AP1000_TLS_WLMIN[2]]
AP1000_TLS_FRMAX = [VACCUM_LIGHT_SPEED / AP1000_TLS_WLMAX[0], None, VACCUM_LIGHT_SPEED / AP1000_TLS_WLMAX[2]]

#                         ERBIUM AMPLIFIER CONSTANTS
# ------------------------------------------------------------------------------
# [3370 : PRE-AMPLIFIER, 3371 : BOOSTER APMLIFIER, 3372 : IN-NINE AMPLIFIER]
# MAX PUMP LASER CURRENT (mA)
AP1000_EFA_IPMAX = [600, 1000, 600]

#                               AP2050 CONSTANTS
# ------------------------------------------------------------------------------
# MIN AND MAX WAVELENGTH
AP2050_WLMIN = 1526
AP2050_WLMAX = 1566
# MIN AND MAX SPAN IN WAVELENGTH
AP2050_MINSPAN = 0.01
AP2050_MAXSPAN = 40

#                               AP2040 CONSTANTS
# ------------------------------------------------------------------------------
# MIN AND MAX WAVELENGTH
AP2040_WLMIN = 1526
AP2040_WLMAX = 1566
# MIN AND MAX WAVELENGTH SPAN
AP2040_MINSPAN = 0.01
AP2040_MAXSPAN = 40
# MIN AND MAX CENTER WAVELENGTH
AP2040_MAXCENTER = AP2040_WLMAX - AP2040_MINSPAN / 2
AP2040_MINCENTER = AP2040_WLMIN + AP2040_MINSPAN / 2
# MIN AND MAX Y RESOLUTION
AP2040_MINYRES = 0.001
AP2040_MAXYRES = 100
# MIN AND MAX POINTS NUMBER
AP2040_MINNPTS = 2
AP2040_MAXNPTS = 20000



#                            ERROR NUMBER CONSTANTS
# ------------------------------------------------------------------------------
APXXXX_ERROR_COMMUNICATION = -1
APXXXX_ERROR_BADCOMMAND = -2
APXXXX_ERROR_ARGUMENT_TYPE = -11
APXXXX_ERROR_ARGUMENT_VALUE = -12
AP1000_ERROR_COMMUNICATION = -1
AP1000_ERROR_BADCOMMAND = -2
AP1000_ERROR_ARGUMENT_TYPE = -11
AP1000_ERROR_ARGUMENT_VALUE = -12
AP1000_ERROR_SLOT_NOT_DEFINED = -151
AP1000_ERROR_SLOT_NOT_GOOD_TYPE = -152
AP1000_ERROR_SLOT_TYPE_NOT_DEFINED = -153
AP1000_ERROR_VARIABLE_NOT_DEFINED = -301

#                          CONSTANTS FOR SIMULATION
# ------------------------------------------------------------------------------
SimuAP1000_ID = "APEX-TECHNOLOGIES/AP1000-8/00001/1.0\n"
SimuAP1000_SlotID = "APEX-TECHNOLOGIES/3314/13-3314-A-13-000502/1.0\n"
SimuAP1000_SlotUsed = "1\n"

SimuPWM_SlotID = "APEX-TECHNOLOGIES/3314/13-3314-A-13-000502/1.0\n"
SimuPWM_AvgTime = "1000\n"
SimuPWM_Wavelength = "1550.000\n"
SimuPWM_Power_dBm = "2.45\n"
SimuPWM_Power_mW = "1.85\n"

SimuATT_SlotID = "APEX-TECHNOLOGIES/3364/12-3364-A-2-000504/0.0\n"
SimuATT_Attenuation = "10\n"
SimuATT_Wavelength = "1528\n"

SimuTLS_SlotID = "APEX-TECHNOLOGIES/3350/10-3350-A-000503/0.0\n"
SimuTLS_Power = "5\n"
SimuTLS_Wavelength = "1553.310\n"

SimuEFA_SlotID = "APEX-TECHNOLOGIES/3371/09-3371-A-000500/0.0\n"
SimuEFA_InVoltage = "512\n"
SimuEFA_OutVoltage = "624\n"
SimuEFA_InPower = "-10\n"
SimuEFA_OutPower = "15\n"

SimuAP2050_ID = "APEX Technologies/2050-A/09-2050-A-000000/9.14\n"
SimuAP2050_StartWavelength = "1526.000\n"
SimuAP2050_StopWavelength = "1566.000\n"
SimuAP2050_Span = "20\n"
SimuAP2050_Center = "1551.234\n"
SimuAP2050_XResolution = "0.100\n"
SimuAP2050_YResolution = "2.000\n"
SimuAP2050_NPoints = "10000\n"

SimuAP2040_ID = "APEX Technologies/2041-B/14-2041-B-000601/9.27\n"
     
