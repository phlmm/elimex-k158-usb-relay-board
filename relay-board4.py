#!/usr/bin/env python3
'''
Based on https://slomkowski.eu/tutorials/eavesdropping-usb-and-writing-driver-in-python/
with device k158: https://elimex.bg/product/49275-kit-k158-usb-interfeys-za-upravlenie-na-4-releta
'''
import argparse

import time
import sys

import usb.core
import usb.util

VENDOR_ID = 0x5053
DEVICE_ID = 0x0002

MANUFACTURER_NAME = "PASAT ELECTRONICS-Bulgaria"
PRODUCT_NAME = "Relay Board-4"

def required_length(nmin,nmax):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin<=len(values)<=nmax:
                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest,nmin=nmin,nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength

def get_args(argv=None):
    parser = argparse.ArgumentParser(description='Turn on /off relays on elimax board')
    parser.add_argument('relay',  type=int, choices = range(1,5))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--on',  help='cmd on', dest='cmd',  action='store_true')
    group.add_argument('--off', help='cmd off', dest='cmd', action='store_false')
    args = parser.parse_args()
    return args

def check_manufacturer_and_product(dev):
    return dev.manufacturer == MANUFACTURER_NAME and dev.product == PRODUCT_NAME


def find_device_handle():
    return usb.core.find(idVendor=VENDOR_ID, idProduct=DEVICE_ID,
                         custom_match=check_manufacturer_and_product)

def set_relay(dev_handle, relay_state):
    dev_handle.ctrl_transfer(0x40, 0x1, relay_state, 0, 0, 0)
    
    
def main():
    args = get_args()
    dev_handle = find_device_handle()
    if (dev_handle == None):
        sys.exit("Could not find device!")

    if dev_handle.is_kernel_driver_active(0):
        try:
            dev_handle.detach_kernel_driver(0)
            print("kernel driver detached")
        except usb.core.USBError as e:
            sys.exit("Could not detach kernel driver: %s" % str(e))

    requestType = usb.util.build_request_type(usb.util.CTRL_OUT,
                                              usb.util.CTRL_TYPE_CLASS,
                                              usb.util.CTRL_RECIPIENT_INTERFACE)

    relay = 0
    if(args.cmd == True):
       relay|=2**(args.relay-1)
    else:
       relay&=2**(args.relay-1) & 0
    set_relay(dev_handle,relay)

if __name__ == "__main__":
    main()
