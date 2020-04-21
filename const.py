'''
Created on 24.02.2020

@author: t.starke
'''

'''
Bilder/Icons
'''
IMG_PATH  = "./icons"
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


'''
GUI Elemente
'''
KNOB_RESIZE_FACTOR = 1
KNOB_ICON_FACTOR = 0.75

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

CRITICAL_SPACE = 50000 # Schwelle in KB ab wann Speicher als voll markiert wird

'''
Timerwerte
'''
COUNTDOWN_START = 5 # Sekunden
BIST_INTERVAL = 5000 # Millisekunden