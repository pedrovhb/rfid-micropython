

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl    
import esp

import mfrc522
import umqtt_simple
import rfid_nersd
import network


esp.osdebug(None)
webrepl.start()
gc.collect()

