# UART Control
#
# This example shows how to use the serial port on your OpenMV Cam. Attach pin
# P4 to the serial input of a serial LCD screen to see "Hello World!" printed
# on the serial LCD display.

import time
from pyb import UART

# Always pass UART 3 for the UART number for your OpenMV Cam.
# The second argument is the UART baud rate. For a more advanced UART control
# example see the BLE-Shield driver.
uart = UART(1)
uart.init(230400, bits=8, parity=None, stop=1)

while(True):
    bytes = uart.read();
    if (bytes != None and len(bytes) > 0):
        s = str(bytes,'UTF-8')
        print(s)
        uart.write('Cone, 100, 200, 0.5, Cube, 150, 120, 0.8\n');

    time.sleep_ms(30);
    print(".");
