import face_recognition
import cv2
import numpy as np
import pickle

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
ryan_image = face_recognition.load_image_file("ryan.jpg")
ryan_face_encoding = face_recognition.face_encodings(ryan_image)[0]

trey_image = face_recognition.load_image_file("trey.jpg")
trey_face_encoding = face_recognition.face_encodings(trey_image)[0]

brody_image = face_recognition.load_image_file("brody.jpg")
brody_face_encoding = face_recognition.face_encodings(brody_image)[0]

ram_image = face_recognition.load_image_file("ram.jpg")
ram_face_encoding = face_recognition.face_encodings(ram_image)[0]

tobin_image = face_recognition.load_image_file("tobin.jpg")
tobin_face_encoding = face_recognition.face_encodings(tobin_image)[0]


file = "trained_model.pkl"

# Encodings
with open(file, 'wb') as f:
    pickle.dump(ryan_face_encoding, f)
    pickle.dump(trey_face_encoding, f)
    pickle.dump(brody_face_encoding, f)
    pickle.dump(ram_face_encoding, f)
    pickle.dump(tobin_face_encoding, f)
