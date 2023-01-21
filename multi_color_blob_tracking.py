# Multi Color Blob Tracking Example
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import sensor, image, time, math
from pyb import UART

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green things. You may wish to tune them...
thresholds = [(30, 100, 0, 25, 30, 60), #Cone_thresholds
              (15, 60, 20,40, -65, -40)] #Cube_thresholds
# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()
uart = UART(1)
uart.init(230400, bits=8, parity=None, stop=1)

def send_targets(targets):
    output = ""
    for i in range(len(targets)):
        output.join("{type}, {imagex}, {imagey}, {confidence}".format(type = targets[i][0], imagex = targets[i][1], imagey = targets[i][2], confidence = targets[i][3]))
        if i < len(targets) -1:
            output.join(",")

    output.join("\n")
    uart.write(output)

while(True):
    clock.tick()
    img = sensor.snapshot()
    targets = []
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        img.draw_rectangle(blob.rect())
        if blob.code() == 1:
            targets.append(["Cone", blob.cx(), blob.cy(), blob.density()])
        else:
            targets.append(["Cube", blob.cx(), blob.cy(), blob.density()])

    send_targets(targets)
        # Note - the blob rotation is unique to 0-180 only
    print(clock.fps())
