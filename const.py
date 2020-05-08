'''
Created on 24.02.2020

@author: t.starke
'''
import os


'''
Bilder/Icons
'''
BASE_PATH = os.path.dirname(__file__)
INI_FILE = BASE_PATH + "/fotobox.ini"

IMG_PATH  = BASE_PATH + "/icons"

# print("icon-path: ", IMG_PATH)
IMG_CK_OFF = IMG_PATH + "/checkbox_checked.png"
IMG_CK_ON = IMG_PATH + "/checkbox_unchecked.png"
IMG_ABORT = IMG_PATH + "/abort_trash.png"
IMG_WARN  = IMG_PATH + "/attention.png"
IMG_ERR   = IMG_PATH + "/attention.png"
IMG_CAM   = IMG_PATH + "/camwhite.png"
IMG_GEAR  = IMG_PATH + "/config_gear.png"
IMG_OK    = IMG_PATH + "/okay.png"

IMG_SD          = IMG_PATH + "/sd_card.png"
IMG_SD_FULL     = IMG_PATH + "/sd_warning.png"
IMG_SD_MISSING  = IMG_PATH + "/sd_missing.png"
IMG_USB         = IMG_PATH + "/usb_stick.png"
IMG_USB_FULL    = IMG_PATH + "/usb_warning.png"
IMG_USB_MISSING = IMG_PATH + "/usb_missing.png"

CHECKBOX_SIZE = 40  # Groesse der Checkboxen im Config-Menue

'''
Status der Applikation
'''
STATE_ERROR = -1 # Kamera fehlt, kann kein Liveview etc.
STATE_LIVE  = 0 # live-view, wartet auf knopf 'start'
STATE_COUNT = 1 # countdown zahlt runter
STATE_BILD  = 2 # bild wird angezeigt, warte auf bestaetigung/abbruch
STATE_IDLE  = 3 # nichts machen

'''
Status der Speicher
'''
MEMSTATE_INIT = -1
MEMSTATE_OK = 0
MEMSTATE_FULL = 1
MEMSTATE_MISSING = 2
