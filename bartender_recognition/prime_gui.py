# GUI WITHOUT VIDEO PROBLEMS

import sys
import time
from random import randint
import cv2
import numpy as np
import Jetson.GPIO as GPIO
import argparse
import os
import platform
import numpy as np
import cv2
import face_recognition
from scipy import False_
import video_pipeline
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStackedWidget,
    QStackedLayout,
)
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont, QImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime

# GLOBAL VARIABLES ####----------------------------------------------------------------------
known_face_encodings = []
known_face_metadata = []

# Set up GPIO
GPIO.setmode(GPIO.BOARD)  # Other options are BCM, CVM, and TEGRA_SOC

bit1 = 36
bit2 = 38
bit3 = 40

GPIO.setup(bit1, GPIO.OUT)
GPIO.setup(bit2, GPIO.OUT)
GPIO.setup(bit3, GPIO.OUT)
GPIO.setup(7, GPIO.IN)

bsize = 233
hsize = 79
vsize = 15
buf = 33
width = 1024
height = 600
startheight = 300
startwidth = 500

# MAIN ####----------------------------------------------------------------------


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setGeometry(0, 0, 1024, 600)
    # w.setGeometry(100, 100, 720, 480)
    w.show()
    app.exec()


# IR SENSOR ####----------------------------------------------------------------------


def cup_close():
    if GPIO.input(7) == 0:
        return True
    else:
        return False


# FACE RECOGNITION ####----------------------------------------------------------------------


def running_on_jetson_nano():
    return platform.machine() == "aarch64"


def register_new_face(face_encoding, face_index, face_image):
    known_face_encodings.append(face_encoding)
    known_face_metadata.append({
        "face_index": face_index,
        "face_image": face_image
    })


def lookup_known_face(face_encoding):
    metadata = None

    if len(known_face_encodings) == 0:
        return metadata

    face_distances = face_recognition.face_distance(
        known_face_encodings,
        face_encoding
    )

    best_match_index = np.argmin(face_distances)

    if face_distances[best_match_index] < 0.6:
        metadata = known_face_metadata[best_match_index]

    return metadata

def binary_known_face(face_encoding):
    metadata = None

    if len(known_face_encodings) == 0:
        return metadata

    face_distances = face_recognition.face_distance(
        known_face_encodings,
        face_encoding
    )

    best_match_index = np.argmin(face_distances)

    if face_distances[best_match_index] < 0.52:
        metadata = known_face_metadata[best_match_index]

    print("Face Distance")
    print(face_distances[0])

    if metadata == None:
        return False
    else:
        return True


def capture_faces(frame, face_locations, face_encodings, margin=0):
    # loop through and save faces in photo
    print("Number of faces:", len(face_locations))
    index = 0
    indicies = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # resize crop bounds
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # add margin around crop area
        top -= margin
        right += margin
        bottom += margin
        left += margin

        # crop to face
        face_frame = frame[top:bottom, left:right]
        face_frame = cv2.resize(face_frame, (150, 150))

        # add to instance of known faces
        index += 1
        register_new_face(face_encoding, index, face_frame)
        print("Face", index, "saved")


def capture_mode(margin=0):
    # Initialize loop variables
    print("Starting capture_mode")
    window_title = "Position faces for photo capture"
    model = 'hog'

    # Clear face encodings from previous instance
    print("Clearing face encodings...")
    known_face_encodings.clear()
    known_face_metadata.clear()

    # start video stream
    print("Starting Pipeline...")
    if running_on_jetson_nano():
        model = 'cnn'
        video_capture = cv2.VideoCapture(
            video_pipeline.gstreamer_pipeline(flip_method=2, frameskip=4), cv2.CAP_GSTREAMER)
    else:
        video_capture = cv2.VideoCapture(0)

    print("Using model:", model)

    if video_capture.isOpened():
        try:
            print("Window Handle")
            # window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            # Identify faces in photo for capture
            face_locations = []
            process_this_frame = True
            print("Starting loop...")
            count = 0;
            while True and count < 100:
                # grab frame of video
                count = count + 1
                print("Capturing Images...")
                ret, frame = video_capture.read()

                # timer = time.time()
                # frame = 0
                # while np.sum(frame) == 0:
                #     print("Pulling Camera Frame...")
                #     ret, frame = video_capture.read()
                #     if time.time() - timer < 10:
                #         print("Camera Failed To Open...")
                #         return False;

                if np.shape(frame) != ():
                    # Resize frame of video to 1/2 size for faster face recognition processing
                    print("Resizing Image...")
                    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                    print("Converting BGR to RGB...")
                    rgb_small_frame = small_frame[:, :, ::-1]

                    print("Finding Faces...")
                    if process_this_frame:
                        # Find all the faces and face encodings in the current frame of video
                        face_locations = face_recognition.face_locations(
                            rgb_small_frame, number_of_times_to_upsample=0, model=model)
                        face_encodings = face_recognition.face_encodings(
                            rgb_small_frame, face_locations)

                        # label all faces in frame
                        face_names = []
                        index = 0
                        for face_location, face_encoding in zip(face_locations, face_encodings):

                            index += 1
                            face_names.append("Face " + str(index))

                    process_this_frame = not process_this_frame

                    # Display live capture preview
                    # for (top, right, bottom, left), label in zip(face_locations, face_names):
                    #     # print("Found face!")
                    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    #     top *= 2
                    #     right *= 2
                    #     bottom *= 2
                    #     left *= 2

                    #     # Draw a box around the face
                    #     cv2.rectangle(frame, (left, top),
                    #                   (right, bottom), (0, 0, 255), 2)

                    #     # Draw a label with a name below the face
                    #     cv2.rectangle(frame, (left, bottom - 35),
                    #                   (right, bottom), (0, 0, 255), cv2.FILLED)
                    #     font = cv2.FONT_HERSHEY_DUPLEX
                    #     cv2.putText(frame, label, (left + 6, bottom - 6),
                    #                 font, 1.0, (255, 255, 255), 1)

                    # # Display the resulting image
                    # if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    #     cv2.imshow(window_title, frame)
                    # else:
                    #     # quit loop if window is forcibly closed
                    #     break

                    keyCode = cv2.waitKey(10) & 0xFF
                    # Hit 'space' on the keyboard to capture photos!
                    # if keyCode == 32:
                    #     print("capturing photo...")
                    #     capture_faces(frame, face_locations,
                    #                   face_encodings, margin)
                    #     break
                    print("capturing photo...")
                    capture_faces(frame, face_locations, face_encodings, margin)
                    if(len(face_locations) >= 1):
                        print("Face Found!")
                        print("Closing live_video...")
                        video_capture.release()
                        cv2.destroyAllWindows()
                        return
                        break
                    else:
                        print("No Face Detected...")

                    # Hit 'q' on the keyboard to quit!
                    if keyCode == ord('q'):
                        print("exiting loop...")
                        break

            # save photos from capture
        finally:
            print("Closing capture_mode...")
            video_capture.release()
            cv2.destroyAllWindows()
        return
    else:
        print("Error: Unable to open camera")
        return False
    return False


def live_video(self):

    print("starting live_video")
    window_title = "Live Video"
    break_cond = False
    model = 'hog'

    # initialize camera stream
    if running_on_jetson_nano():
        model = 'cnn'
        video_capture = cv2.VideoCapture(
            video_pipeline.v4l_pipeline(frameskip=2), cv2.CAP_GSTREAMER)
    else:
        video_capture = cv2.VideoCapture(0)

    print("Using model:", model)

    if video_capture.isOpened():
        try:
            # print("Error heeerrrrreeee")
            # window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

            # Identify faces in photo for capture
            face_locations = []
            process_this_frame = True
            print("Starting loop...")
            while True:
                # grab frame of video
                print("Getting Frame")
                ret, frame = video_capture.read()

                # print("Showing Image")

                # cv2.imshow('image', frame);

                # Resize frame of video to 1/2 size for faster face recognition processing
                print('Resizing Frame...')
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                print("Converting BGR into RGB...")
                rgb_small_frame = small_frame[:, :, ::-1]

                print("Frame Processed Successfully!")
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(
                        rgb_small_frame, number_of_times_to_upsample=0, model=model)
                    # face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=0, model=model)
                    # face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(
                        rgb_small_frame, face_locations)

                    # label all faces in frame
                    face_names = []
                    for face_location, face_encoding in zip(face_locations, face_encodings):

                        metadata = lookup_known_face(face_encoding)

                        if metadata is not None:
                            face_label = f"Face {int(metadata['face_index'])}"
                        else:
                            face_label = "Unknown"

                        face_names.append(face_label)

                process_this_frame = not process_this_frame

                print("capturing photo...")
                margin = 0
                # capture_faces(frame, face_locations, face_encodings, margin)
                if(len(face_locations) >= 1):
                    for i in face_encodings:
                        print("Looking Up Face")
                        print(lookup_known_face(i))
                        print("-")
                        print(face_encodings)
                        print("Face Found! Face 1! Moving to Order Menu")
                        print("Closing live_video...")
                        video_capture.release()
                        cv2.destroyAllWindows()
                    return i
                    break
                else:
                    print("No Face Detected...")

                # Hit 'q' on the keyboard to quit!
                # if keyCode == ord('q'):
                #     print("exiting loop...")
                #     break_cond = True
                #     break
        finally:
            print("Closing live_video...")
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")

    return break_cond

# PyQt5 ####------------------------------------------------------------------------------


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Bartender Gui")

        # top-level layout
        w = QWidget()
        layout = QVBoxLayout()

        self.setLayout(layout)
        # create stacked layout
        self.stackedLayout = QStackedLayout()

        # create and connect window navigation
        # approach window
        approach_widget = ApproachWidget(self)
        approach_widget.button.clicked.connect(self.scan_window)
        self.stackedLayout.addWidget(approach_widget)
        # scan window
        scan_widget = ScanWidget(self)
        # scan_widget.scan_button.clicked.connect(self.order_window)
        scan_widget.exit_button.clicked.connect(self.approach_window)
        self.stackedLayout.addWidget(scan_widget)
        # order window
        order_widget = OrderWidget(self)
        self.stackedLayout.addWidget(order_widget)
        # verify cup window
        verify_widget = VerifyWidget(self)
        self.stackedLayout.addWidget(verify_widget)
        # remove cup window
        remove_widget = RemoveCupWidget(self)
        self.stackedLayout.addWidget(remove_widget)

        # make stacked layout central widget
        layout.addLayout(self.stackedLayout)

    def approach_window(self):
        print("Opening approach menu")
        self.stackedLayout.setCurrentIndex(0)

    def scan_window(self):
        print("Opening scan menu")
        # self.video_thread.video_preview()
        self.stackedLayout.setCurrentIndex(1)
        # time.sleep(3)
        # self.video_thread.video_preview()
        # self.layout.stackedLayout.scan_widget.video_feed(self)

    def order_window(self):
        print("Opening order menu")
        self.stackedLayout.setCurrentIndex(2)

    def verify_cup(self):
        print("Verifying cup placement")
        self.stackedLayout.setCurrentIndex(3)
        QApplication.processEvents()
        # QApplication.processEvents()
        # loop until cup placement verified
        # time.sleep(5) # placeholder
        # self.order_window()


    def remove_cup(self):
        print("Remove cup prompt")
        self.stackedLayout.setCurrentIndex(4)
        # loop until cup removal is verified
        # time.sleep(5) # placeholder

    def closeEvent(self, event):
        # self.video_thread.shutdown()
        event.accept()


class ApproachWidget(QWidget):
    def __init__(self, parent=None):
        super(ApproachWidget, self).__init__(parent)
        w = QWidget()
        self.button = QPushButton(w)
        self.button.setFont(QFont('Calibri', 30))
        self.button.setText("Place Order")
        self.button.setGeometry(0, 0, startwidth, startheight)
        # self.button.move(width/2-startwidth/2, height/2 - startheight/2)
        self.button.setGeometry(0, 0, 900, 40)
        self.button.move(62, 500)
        layout = QVBoxLayout()
        layout.addWidget(w)
        self.button.clicked.connect(self.enter_function)
        self.setLayout(layout)

        self.label1 = QLabel(w)
        pixmap = QPixmap('Menu Home Green.png')
        # smaller_pixmap = pixmap.scaled(1000, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap(pixmap)
        self.label1.move(62, 0)

        layout.addWidget(w)
        self.setLayout(layout)

    def enter_function(self):
        print("Place Order button clicked")
        self.parent().scan_window()


class ScanWidget(QWidget):
    def __init__(self, parent=None):
        super(ScanWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        w = QWidget()

        # scan button
        self.scan_button = QPushButton(w)
        self.scan_button.setFont(QFont('Arial', 16))
        self.scan_button.setText("Scan ID")
        self.scan_button.setGeometry(0, 0, 900, 40)
        # self.scan_button.move(62, 4*vsize + 2*bsize + buf - 72)
        self.scan_button.move(62, 440)
        self.scan_button.clicked.connect(self.scan_function)

        # exit button
        self.exit_button = QPushButton(w)
        self.exit_button.setFont(QFont('Arial', 16))
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(0, 0, 900, 40)
        self.exit_button.move(62, 500)
        # self.exit_button.move(62, 0 + buf - 20)
        self.exit_button.clicked.connect(self.exit_function)

        self.layout_hor = QHBoxLayout()

        self.label1 = QLabel(w)
        pixmap = QPixmap('Menu v1.png')
        # smaller_pixmap = pixmap.scaled(1000, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap(pixmap)
        self.label1.move(62, 0)
        # self.layout_hor.addWidget(self.label1)

        self.label2 = QLabel(w)
        pixmap = QPixmap('Menu w1.png')
        # smaller_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap(pixmap)
        # self.layout_hor.addWidget(self.label2)
        self.label2.move(562, 0)

        # self.layout.addLayout(self.layout_hor)
        # label1.setGeometry(100, 200, 300, 80)
        # self.resize(pixmap.width(), 0.5*pixmap.height())

        self.layout.addWidget(w)
        self.setLayout(self.layout)

    def scan_function(self):
        print("Scan ID clicked")
        print("Capture Mode")
        pixmap = QPixmap('Menu v4.png')
        self.label1.setPixmap(pixmap)
        QApplication.processEvents()
        time.sleep(1)
        ret = capture_mode()
        print(ret);
        if ret == False:
        # if False:
            print("Changing to Approach Window")
            pixmap = QPixmap('Menu v3.png')
            self.label1.setPixmap(pixmap)
            QApplication.processEvents()
            time.sleep(5)
            self.parent().approach_window()
        else:
            pixmap = QPixmap('Menu v2.png')
            self.label1.setPixmap(pixmap)
            QApplication.processEvents()
            time.sleep(1)

            pixmap = QPixmap('Menu w2.png')
            self.label2.setPixmap(pixmap)
            QApplication.processEvents()
            time.sleep(1)

            face = live_video(self)
            correct_face = False
            print("FACE:")
            print(face);
            print("FACE #1:")
            print(known_face_encodings)
            print("------------")
            if binary_known_face(face) == True:
            # if True:
                print("Known Face Found. ID Approved");
                pixmap = QPixmap('Menu w3.png')
                self.label2.setPixmap(pixmap)
                QApplication.processEvents()
                time.sleep(1)
                self.parent().verify_cup()
            else:
                print("No Known Faces Found. ID Rejected.")
                pixmap = QPixmap('Menu w4.png')
                self.label2.setPixmap(pixmap)
                QApplication.processEvents()
                time.sleep(3)
                self.parent().approach_window()

            #Reset Window For Next User
            pixmap = QPixmap('Menu v1.png')
            self.label1.setPixmap(pixmap)
            pixmap = QPixmap('Menu w1.png')
            self.label2.setPixmap(pixmap)


    def exit_function(self):
        print("Exit button clicked")
        # print("Stopping video preview")

class VerifyWidget(QWidget):
    def __init__(self, parent=None):
        super(VerifyWidget, self).__init__(parent)
        w = QWidget()
        self.layout = QVBoxLayout()

        self.continue_button = QPushButton(w)
        # self.continue_button.setFont(QFont('Calibri', 30))
        self.continue_button.setFont(QFont('Arial', 16))
        self.continue_button.setText("Continue...")
        self.continue_button.setGeometry(0, 0, 900, 40)
        # self.scan_button.move(62, 4*vsize + 2*bsize + buf - 72)
        self.continue_button.move(62, 440)
        self.layout = QVBoxLayout()
        self.layout.addWidget(w)
        self.continue_button.clicked.connect(self.cup_placed)
        self.setLayout(self.layout)
        
        self.exit_button = QPushButton(w)
        self.exit_button.setFont(QFont('Arial', 16))
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(0, 0, 900, 40)
        self.exit_button.move(62, 500)
        # self.exit_button.move(62, 0 + buf - 20)
        self.exit_button.clicked.connect(self.exit_function)

        self.label1 = QLabel(w)
        pixmap = QPixmap('Menu x1.png')
        # smaller_pixmap = pixmap.scaled(1000, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap(pixmap)
        self.label1.move(62, 0)

        self.layout.addWidget(w)
        self.setLayout(self.layout)

    def cup_placed(self):
        #Check if placed, if so continue
        check_placement = cup_close() #PUT FUNCTION CALL HERE
        if check_placement:
            #In the correct spot
            print("Cup Placed Correctly");
            pixmap = QPixmap('Menu x2.png')
            self.label1.setPixmap(pixmap)
            QApplication.processEvents()
            time.sleep(2);
            pixmap = QPixmap('Menu x1.png')
            self.label1.setPixmap(pixmap)
            self.parent().order_window()
        else:
            print("Cup Placed Incorrectly...Try Again");
            pixmap = QPixmap('Menu x3.png')
            self.label1.setPixmap(pixmap)
            QApplication.processEvents()

    def exit_function(self):
        print("Exit button clicked")
        self.parent().approach_window()
        # print("Stopping video preview")
            

class RemoveCupWidget(QWidget):
    def __init__(self, parent=None):
        super(RemoveCupWidget, self).__init__(parent)
        w = QWidget()
        self.layout = QVBoxLayout()

        self.done_button = QPushButton(w)
        # self.continue_button.setFont(QFont('Calibri', 30))
        self.done_button.setFont(QFont('Arial', 16))
        self.done_button.setText("Finish Order")
        self.done_button.setGeometry(0, 0, 900, 80)
        # self.scan_button.move(62, 4*vsize + 2*bsize + buf - 72)
        self.done_button.move(62, 440)
        self.layout = QVBoxLayout()
        self.layout.addWidget(w)
        self.done_button.clicked.connect(self.cup_removed)
        self.setLayout(self.layout)

        self.label1 = QLabel(w)
        pixmap = QPixmap('Menu z1.png')
        # smaller_pixmap = pixmap.scaled(1000, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap(pixmap)
        self.label1.move(62, 0)

        self.layout.addWidget(w)
        self.setLayout(self.layout)

    def cup_removed(self):
        #Check if placed, if so continue
        check_placement = cup_close() #PUT FUNCTION CALL HERE
        if check_placement == False:
            #In the correct spot
            print("Cup Removed Correctly");
            pixmap = QPixmap('Menu z2.png')
            self.label1.setPixmap(pixmap)
            QApplication.processEvents()
            time.sleep(3);
            pixmap = QPixmap('Menu z1.png')
            self.label1.setPixmap(pixmap)
            self.parent().approach_window()
        else:
            print("Cup Not Removed...Try Again");
            pixmap = QPixmap('Menu z3.png')
            self.label1.setPixmap(pixmap)
            QApplication.processEvents()

class OrderWidget(QWidget):
    def __init__(self, parent=None):
        super(OrderWidget, self).__init__(parent)
        w = QWidget()
        self.layout = QVBoxLayout()

        #  TOP ROW

        # button 1
        self.button1 = QPushButton(w)
        self.button1.setGeometry(0, 0, bsize, bsize)
        self.button1.setFont(QFont('Calibri', 25))
        self.button1.setText("Ginger Beer")
        self.button1.move(hsize, vsize+buf)
        self.button1.clicked.connect(self.button1_clicked)

        # button 2
        self.button2 = QPushButton(w)
        self.button2.setGeometry(0, 0, bsize, bsize)
        self.button2.setFont(QFont('Calibri', 25))
        self.button2.setText("Cape Codder")
        self.button2.move(2*hsize + bsize, vsize+buf)
        self.button2.clicked.connect(self.button2_clicked)

        # button 3
        self.button3 = QPushButton(w)
        self.button3.setGeometry(0, 0, bsize, bsize)
        self.button3.setFont(QFont('Calibri', 25))
        self.button3.setText("Pearl Harbor")
        self.button3.move(3*hsize + 2*bsize, vsize+buf)
        self.button3.clicked.connect(self.button3_clicked)

        # button 4
        self.button4 = QPushButton(w)
        self.button4.setGeometry(0, 0, bsize, bsize)
        self.button4.setFont(QFont('Calibri', 25))
        self.button4.setText("Screwdriver")
        self.button4.move(3*hsize + 2*bsize, 2*vsize+bsize+buf)
        self.button4.clicked.connect(self.button4_clicked)

        #  BOTTOM ROW

        # button 5
        self.button5 = QPushButton(w)
        self.button5.setGeometry(0, 0, bsize, bsize)
        self.button5.setFont(QFont('Calibri', 25))
        self.button5.setText("Madras")
        self.button5.move(hsize, 2*vsize+bsize+buf)
        self.button5.clicked.connect(self.button5_clicked)

        # button 6
        self.button6 = QPushButton(w)
        self.button6.setGeometry(0, 0, bsize, bsize)
        self.button6.setFont(QFont('Calibri', 25))
        self.button6.setText("~Stuff on the Beach~")
        self.button6.move(2*hsize + bsize,  2*vsize+bsize+buf)
        self.button6.clicked.connect(self.button6_clicked)

        # # button 7
        # self.button7 = QPushButton(w)
        # self.button7.setGeometry(0, 0, bsize, bsize)
        # self.button7.setText("Drink 7")
        # self.button7.move(3*hsize + 2*bsize,  2*vsize+bsize+buf)
        # self.button7.clicked.connect(self.button7_clicked)

        # # button 8
        # self.button8 = QPushButton(w)
        # self.button8.setGeometry(0, 0, bsize, bsize)
        # self.button8.setText("Drink 8")
        # self.button8.move(4*hsize + 3*bsize,  2*vsize+bsize+buf)
        # self.button8.clicked.connect(self.button8_clicked)

        # self.label1 = QLabel(w)
        # pixmap = QPixmap('Menu blank.png')
        # # smaller_pixmap = pixmap.scaled(1000, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        # self.label1.setPixmap(pixmap)
        # self.label1.move(62, 0)

        self.layout.addWidget(w)
        self.setLayout(self.layout)

    def button1_clicked(self):
        print("Button 1 clicked")
        # pixmap = QPixmap('Menu y1.png')
        # self.label1.setPixmap(pixmap)
        # QApplication.processEvents()
        pumpCall(1)
        # # return to approach menu
        # time.sleep(1)
        # pixmap = QPixmap('Menu y2.png')
        # self.label1.setPixmap(pixmap)
        # QApplication.processEvents()
        # time.sleep(2)
        # time.sleep(1)
        self.parent().remove_cup()

    def button2_clicked(self):
        print("Button 2 clicked")
        # pixmap = QPixmap('Menu y1.png')
        # self.label1.setPixmap(pixmap)
        # QApplication.processEvents()
        pumpCall(2)
        # # return to approach menu
        # time.sleep(1)
        # pixmap = QPixmap('Menu y2.png')
        # self.label1.setPixmap(pixmap)
        # QApplication.processEvents()
        # time.sleep(2)
        # time.sleep(1)
        self.parent().remove_cup()

    def button3_clicked(self):
        print("Button 3 clicked")
        pumpCall(3)
        # return to approach menu
        time.sleep(1)
        self.parent().remove_cup()

    def button4_clicked(self):
        print("Button 4 clicked")
        pumpCall(4)
        # return to approach menu
        time.sleep(1)
        self.parent().remove_cup()

    def button5_clicked(self):
        print("Button 5 clicked")
        pumpCall(5)
        # return to approach menu
        time.sleep(1)
        self.parent().remove_cup()

    def button6_clicked(self):
        print("Button 6 clicked")
        pumpCall(6)
        # return to approach menu
        time.sleep(1)
        self.parent().remove_cup()

    def button7_clicked(self):
        print("Button 7 clicked")
        pumpCall(7)
        # return to approach menu
        time.sleep(1)
        self.parent().remove_cup()

    def button8_clicked(self):
        print("Button 8 clicked")
        pumpCall(8)
        # return to approach menu
        time.sleep(1)
        self.parent().remove_cup()

# Function for pump call


def pumpCall(flag):
    if flag == 1:
      # Write a binary 1
        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, True)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

    elif flag == 2:
        # Write a binary 2 (Cranberry Juice)
        GPIO.output(bit1, False)
        GPIO.output(bit2, True)
        GPIO.output(bit3, False)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

    elif flag == 3:
        # Write a binary 3 (Fanta)
        GPIO.output(bit1, False)
        GPIO.output(bit2, True)
        GPIO.output(bit3, True)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

    elif flag == 4:
        # Write a binary 4
        GPIO.output(bit1, True)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

    elif flag == 5:
        # Write a binary 5
        GPIO.output(bit1, True)
        GPIO.output(bit2, False)
        GPIO.output(bit3, True)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

    elif flag == 6:
        # Write a binary 6
        GPIO.output(bit1, True)
        GPIO.output(bit2, True)
        GPIO.output(bit3, False)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)

    else:
        # Reset to 0
        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)


if __name__ == '__main__':
    os.system("sudo service nvargus-daemon restart");
    main()
