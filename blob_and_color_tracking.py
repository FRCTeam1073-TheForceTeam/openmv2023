# Multi Color Blob Tracking Example
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import sensor, image, time, math
from pyb import UART

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green things. You may wish to tune them...
thresholds = [(30, 100, 0, 25, 30, 60), #Cone_thresholds
              (15, 60, 10,30, -45, -10)] #Cube_thresholds
# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.
#(15, 60, 20,40, -65, -40)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()
uart = UART(1)
uart.init(230400, bits=8, parity=None, stop=1)

# The apriltag code supports up to 6 tag families which can be processed at the same time.
# Returned tag objects will have their tag family and id within the tag family.

tag_families = 0
tag_families |= image.TAG16H5 # comment out to disable this family


# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"

def send_targets(targets):
    output = ""
    num_to_send = len(targets);
    if num_to_send > 10:
        num_to_send = 10;

    for i in range(num_to_send):
        if i < len(targets) -1:
            output += ("{type},{imagex},{imagey},{confidence},{area},".format(type = targets[i][0], imagex = targets[i][1], imagey = targets[i][2], confidence = targets[i][3], area=targets[i][4]))
        else:
            output += ("{type},{imagex},{imagey},{confidence},{area}".format(type = targets[i][0], imagex = targets[i][1], imagey = targets[i][2], confidence = targets[i][3], area=targets[i][4]))

    output += "\n"
    print(output)
    uart.write(output)

while(True):
    clock.tick()
    img = sensor.snapshot()
    targets = []
    for blob in img.find_blobs(thresholds, pixels_threshold=200, area_threshold=200):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        img.draw_rectangle(blob.rect())
        if blob.code() == 1:
            targets.append(["Cone", blob.cx(), blob.cy(), blob.density(), blob.area()])
        else:
            targets.append(["Cube", blob.cx(), blob.cy(), blob.density(), blob.area()])


    for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)

    send_targets(targets)

        # Note - the blob rotation is unique to 0-180 only
    # print(clock.fps())
    #time.sleep_ms(200)
