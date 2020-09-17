# This file is executed on every boot (including wake-boot from deepsleep)
#
import sys
import esp
#esp.osdebug(None)
import uos, machine
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
# import webrepl
# webrepl.start()
gc.collect()
sys.path.append('/main')


reasons = {
    0: "Power On Reset",
    1: "Watchdog Timer Reset",
    4: "Soft Reset",
    5: "Deepsleep Reset",
    6: "Hard Reset"
}

# print ("Machine id: " + hex(machine.unique_id()) )
print ("")
print (uos.uname().machine)
print ("Running verson: " + uos.uname().version)
print ("Reason for reset: " + reasons.get(machine.reset_cause()))
print ("Flash size: " + str(esp.flash_size()))
print ("Free memory: " + str(esp.freemem()))

import app 