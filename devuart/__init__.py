import subprocess
import lxml.etree

from base64 import b64decode
from collections import defaultdict

from .plist import PlistBrowser


def _get_uarts_by_type():
    """
    Query IOKit to discover connected serial devices.

    Returns a
    """
    out = subprocess.check_output(["ioreg", "-talrc", "IOSerialBSDClient"])
    plist = lxml.etree.fromstring(out)

    usb_devs = plist.xpath(
        "//key[text() = 'IOCalloutDevice']/"
        "ancestor::dict["
        "child::key[text() = 'IOObjectClass' and "
        "following-sibling::*[1][text() = 'IOUSBInterface']]]/ancestor::*[1]")

    bt_devs = plist.xpath(
        "//key[text() = 'IOCalloutDevice']/"
        "ancestor::dict["
        "child::key[text() = 'IOObjectClass' and "
        "following-sibling::*[1][text() = 'IOBluetoothSerialClient']]]")

    return {
        "usb": [PlistBrowser(v) for v in usb_devs],
        "bluetooth": [PlistBrowser(v) for v in bt_devs]
    }


def _get_callout_file(dev):
    return dev.find('IOCalloutDevice').value()


def _name_usb_dev(dev):
    vendor = dev.find("USB Vendor Name").value()
    product = dev.find("USB Product Name").value()
    return (vendor, product, "%s %s" % (vendor, product))


def _name_bt_dev(dev):
    try:
        svc_name = dev.find('PortDeviceService').value()
        dev_name = dev.find('PortDeviceName').value()
    except KeyError:
        return ()

    dev_name = b64decode(dev_name).decode('utf8')
    return (svc_name, dev_name)


def get_uart_devices_by_name():
    """
    Query IOKit to discover connected serial devices.

    Returns a dictionary mapping descriptive strings to device paths. The
    descriptive strings available depend on the type of serial device. USB
    devices are indexed by vendor name, product name, and "<vendor>
    <product>". Bluetooth devices are indexed by service name and device name.
    """
    devs_by_type = _get_uarts_by_type()
    devs_by_name = defaultdict(list)
    naming_map = {
        "usb": _name_usb_dev,
        "bluetooth": _name_bt_dev
    }

    for dev_type, devs in devs_by_type.items():
        name_fn = naming_map.get(dev_type)
        if not name_fn:
            continue
        for dev in devs:
            uart = _get_callout_file(dev)
            for name in name_fn(dev):
                devs_by_name[name].append(uart)
    return devs_by_name


def get_uart_by_name(name):
    """
    Query IOKit to discover the callout file for a named serial device.

    Returns the absolute path to the callout file.
    """
    devs = get_uart_devices_by_name()
    matches = list(devs[name])
    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches[0]
    else:
        return matches
