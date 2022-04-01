import face_recognition
import cv2
import numpy as np

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

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Load a sample picture and learn how to recognize it.
# train_dir = "./train_dir/"
ryan_image = face_recognition.load_image_file("./train_dir/ryan.jpg")
ryan_face_encoding = face_recognition.face_encodings(ryan_image)[0]

trey_image = face_recognition.load_image_file("./train_dir/trey.jpg")
trey_face_encoding = face_recognition.face_encodings(trey_image)[0]

brody_image = face_recognition.load_image_file("./train_dir/brody.jpg")
brody_face_encoding = face_recognition.face_encodings(brody_image)[0]

ram_image = face_recognition.load_image_file("./train_dir/ryan.jpg")
ram_face_encoding = face_recognition.face_encodings(ram_image)[0]

tobin_image = face_recognition.load_image_file("./train_dir/tobin.jpg")
tobin_face_encoding = face_recognition.face_encodings(tobin_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    ryan_face_encoding,
    trey_face_encoding,
    brody_face_encoding,
    ram_face_encoding,
    tobin_face_encoding
]
known_face_names = [
    "Ryan",
    "Trey",
    "Brody", 
    "Ram",
    "Tobin"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2),cv2.CAP_GSTREAMER)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        # face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model='cnn')
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
