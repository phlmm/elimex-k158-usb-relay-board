#!/usr/bin/env python3
'''
Based on https://slomkowski.eu/tutorials/eavesdropping-usb-and-writing-driver-in-python/
with device k158: https://elimex.bg/product/49275-kit-k158-usb-interfeys-za-upravlenie-na-4-releta
'''

import time
import sys

import usb.core
import usb.util

VENDOR_ID = 0x5053
DEVICE_ID = 0x0002

MANUFACTURER_NAME = "PASAT ELECTRONICS-Bulgaria"
PRODUCT_NAME = "Relay Board-4"


def check_manufacturer_and_product(dev):
    return dev.manufacturer == MANUFACTURER_NAME and dev.product == PRODUCT_NAME


def find_device_handle():
    return usb.core.find(idVendor=VENDOR_ID, idProduct=DEVICE_ID,
                         custom_match=check_manufacturer_and_product)


dev_handle = find_device_handle()

if dev_handle.is_kernel_driver_active(0):
    try:
        dev_handle.detach_kernel_driver(0)
        print("kernel driver detached")
    except usb.core.USBError as e:
        sys.exit("Could not detach kernel driver: %s" % str(e))

requestType = usb.util.build_request_type(usb.util.CTRL_OUT,
                                          usb.util.CTRL_TYPE_CLASS,
                                          usb.util.CTRL_RECIPIENT_INTERFACE)


def set_relay(relay_state ):
    dev_handle.ctrl_transfer(0x40, 0x1, relay_state, 0, 0, 0)


while True:
    set_relay(1)
    time.sleep(0.2)
    set_relay(1)
    time.sleep(0.2)
    set_relay(2)
    time.sleep(0.2)
    set_relay(2)
    time.sleep(0.2)
    set_relay(4)
    time.sleep(0.2)
    set_relay(4)
    time.sleep(0.2)
    set_relay(8)
    time.sleep(0.2)
    set_relay(8)
    time.sleep(0.2)
