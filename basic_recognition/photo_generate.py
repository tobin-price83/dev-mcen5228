import argparse
import os
import numpy as np
import cv2
import numpy as np
import face_recognition
from PIL import Image

parser = argparse.ArgumentParser(description="Crop photos from a video feed")
# parser.add_argument("-n","--name", help = "name of face captured")
parser.add_argument("-o","--output", help = "filepath of output folder", required = False, default = "./export")
parser.add_argument("-m","--margin", help = "additional margin of crop around detected face", required = False, default = 0)
parser.add_argument("-a","--append", help = "append a suffix to filename", required = False, default = "")

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=640,
    display_height=360,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def capture_photo



if __name__ == '__main__':
	main()