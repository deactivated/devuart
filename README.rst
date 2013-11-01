=======
devuart
=======

`devuart` lets you efficiently look up the path to a serial device
using the device name and manufacturer.

Usage
=====

Retrieve a dictionary mapping from name to device path::

  >>> uarts = devuart.get_uart_devices_by_name()
  >>> pprint(uarts)
   
  {'FireFly-812B': ['/dev/cu.FireFly-812B-SPP'],
   'Microcontroller': ['/dev/cu.usbmodem1d1132'],
   'SPP': ['/dev/cu.FireFly-812B-SPP'],
   'mbed': ['/dev/cu.usbmodem1d1132'],
   'mbed Microcontroller': ['/dev/cu.usbmodem1d1132']}

Look up the device path for a single device::

  >>> devuart.get_uart_by_name("mbed")
  '/dev/cu.usbmodem1d1132'
