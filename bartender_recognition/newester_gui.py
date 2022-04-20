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

#### GLOBAL VARIABLES ####----------------------------------------------------------------------
known_face_encodings = []
known_face_metadata = []

# Set up GPIO
GPIO.setmode(GPIO.BOARD) # Other options are BCM, CVM, and TEGRA_SOC

bit1 = 36
bit2 = 38
bit3 = 40

GPIO.setup(bit1, GPIO.OUT)
GPIO.setup(bit2, GPIO.OUT)
GPIO.setup(bit3, GPIO.OUT)

bsize = 200;
hsize = 45;
vsize = 20;
buf = 25;
width = 1024;
height = 600;
startheight = 300;
startwidth = 500;     

#### MAIN ####----------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setGeometry(0, 0, 1024, 600)
    # w.setGeometry(100, 100, 720, 480)
    w.show()
    app.exec()

#### FACE RECOGNITION ####----------------------------------------------------------------------
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


def capture_faces(frame, face_locations, face_encodings, margin=0):
    # loop through and save faces in photo
    print("Number of faces:", len(face_locations))
    index = 0
    indicies = [];
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
    print("Starting Pipeline...");
    if running_on_jetson_nano():
        model = 'cnn'
        video_capture = cv2.VideoCapture(
            video_pipeline.gstreamer_pipeline(flip_method=2,frameskip=4), cv2.CAP_GSTREAMER)
    else:
        video_capture = cv2.VideoCapture(0)

    print("Using model:", model)

    if video_capture.isOpened():
        try:
            print("Window Handle");
            # window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            # Identify faces in photo for capture
            face_locations = []
            process_this_frame = True
            print("Starting loop...")
            while True:
                # grab frame of video
                print("Capturing Images...");
                ret, frame = video_capture.read()

                # Resize frame of video to 1/2 size for faster face recognition processing
                print("Resizing Image...");
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                print("Converting BGR to RGB...");
                rgb_small_frame = small_frame[:, :, ::-1]

                print("Finding Faces...");
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
                    print("Face Found!");
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
    else:
        print("Error: Unable to open camera")

def live_video(self):

    print("starting live_video")
    window_title = "Live Video"
    break_cond = False
    model = 'hog'

    # initialize camera stream
    if running_on_jetson_nano():
        model = 'cnn'
        video_capture = cv2.VideoCapture(video_pipeline.v4l_pipeline(frameskip=2), cv2.CAP_GSTREAMER)
    else:
        video_capture = cv2.VideoCapture(0)

    print("Using model:", model)

    if video_capture.isOpened():
        try:
            print("Error heeerrrrreeee")
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

                print("Frame Processed Successfully!");
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
                capture_faces(frame, face_locations, face_encodings, margin)
                if(len(face_locations) >= 1):
                    for i in face_encoding:
                        print("Looking Up Face")
                        print(lookup_known_face(i));
                        print("-")
                        print(face_encodings);
                        print("Face Found! Face 1! Moving to Order Menu");
                        print("Closing live_video...")
                        video_capture.release()
                        cv2.destroyAllWindows()
                    return
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

#### PyQt5 ####------------------------------------------------------------------------------
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
        scan_widget.scan_button.clicked.connect(self.order_window)
        scan_widget.exit_button.clicked.connect(self.approach_window)
        self.stackedLayout.addWidget(scan_widget)
        # order window
        order_widget = OrderWidget(self)
        self.stackedLayout.addWidget(order_widget)

        
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

    def closeEvent(self, event):
        # self.video_thread.shutdown()
        event.accept()


class ApproachWidget(QWidget):
    def __init__(self, parent=None):
        super(ApproachWidget, self).__init__(parent)
        w = QWidget()
        self.button = QPushButton(w)
        self.button.setFont(QFont('Calibri',30))
        self.button.setText("Place Order")
        self.button.setGeometry(0,0,startwidth,startheight)
        self.button.move(width/2-startwidth/2, height/2 - startheight/2)
        layout = QVBoxLayout()
        layout.addWidget(w)
        self.button.clicked.connect(self.enter_function)
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
        self.scan_button.setFont(QFont('Arial',16))
        self.scan_button.setText("Scan ID")
        self.scan_button.setGeometry(0,0,900,40)
        # self.scan_button.move(62, 4*vsize + 2*bsize + buf - 72)
        self.scan_button.move(62, 20)
        self.scan_button.clicked.connect(self.scan_function)

        # exit button
        self.exit_button = QPushButton(w)
        self.exit_button.setFont(QFont('Arial',16))
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(0,0,900,40)
        self.exit_button.move(62, 70)
        # self.exit_button.move(62, 0 + buf - 20)
        self.exit_button.clicked.connect(self.exit_function)

        self.layout_hor = QHBoxLayout()

        self.label1 = QLabel(self)
        pixmap = QPixmap('Menu v1.png')
        # smaller_pixmap = pixmap.scaled(1000, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label1.setPixmap(pixmap)
        self.layout_hor.addWidget(self.label1)
        self.label1.move(100, 100)

        self.label2 = QLabel(self)
        pixmap = QPixmap('Menu w1.png')
        # smaller_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label2.setPixmap(pixmap)
        self.layout_hor.addWidget(self.label2)
        self.label2.move(200, 100)

        self.layout.addLayout(self.layout_hor)
        # label1.setGeometry(100, 200, 300, 80)
        # self.resize(pixmap.width(), 0.5*pixmap.height())
        

        self.layout.addWidget(w)
        self.setLayout(self.layout)

    def scan_function(self):
        print("Scan ID clicked")
        print("Capture Mode")
        capture_mode()
        # time.sleep(1)
        pixmap = QPixmap('Menu v2.png')
        # self.label1.move(100, 100)
        self.label1.setPixmap(pixmap)
        QApplication.processEvents()
        # time.sleep(0.5)

        
        pixmap = QPixmap('Menu w2.png')
        # self.label1.move(100, 100)
        self.label2.setPixmap(pixmap)
        QApplication.processEvents()
        time.sleep(3)

        break_cond = live_video(self)

        pixmap = QPixmap('Menu w3.png')
        # self.label1.move(100, 100)
        self.label2.setPixmap(pixmap)
        QApplication.processEvents()
        time.sleep(3)

        # self.parent().video_thread.stop()
        # self.parent().video_thread.stop()
        # self.parent().order_window()

    def exit_function(self):
        print("Exit button clicked")
        # print("Stopping video preview")

    

class OrderWidget(QWidget):
    def __init__(self, parent=None):
        super(OrderWidget, self).__init__(parent)
        w = QWidget()
        layout = QVBoxLayout()

        #  TOP ROW

        # button 1
        self.button1 = QPushButton(w)
        self.button1.setGeometry(0, 0, bsize, bsize)
        self.button1.setText("Drink 1")
        self.button1.move(hsize, vsize+buf)
        self.button1.clicked.connect(self.button1_clicked)

        # button 2
        self.button2 = QPushButton(w)
        self.button2.setGeometry( 0, 0, bsize, bsize)
        self.button2.setText("Drink 2")
        self.button2.move(2*hsize + bsize, vsize+buf)
        self.button2.clicked.connect(self.button2_clicked)

        # button 3 
        self.button3 = QPushButton(w)
        self.button3.setGeometry(0, 0, bsize, bsize)
        self.button3.setText("Drink 3")
        self.button3.move(3*hsize + 2*bsize, vsize+buf)
        self.button3.clicked.connect(self.button3_clicked)

        # button 4
        self.button4 = QPushButton(w)
        self.button4.setGeometry(0, 0, bsize, bsize)
        self.button4.setText("Drink 4")
        self.button4.move(4*hsize + 3*bsize, vsize+buf)
        self.button4.clicked.connect(self.button4_clicked)


        #  BOTTOM ROW

        # button 5
        self.button5 = QPushButton(w)
        self.button5.setGeometry(0, 0, bsize, bsize)
        self.button5.setText("Drink 5")
        self.button5.move(hsize, 2*vsize+bsize+buf)
        self.button5.clicked.connect(self.button5_clicked)
        
        # button 6
        self.button6 = QPushButton(w)
        self.button6.setGeometry( 0, 0, bsize, bsize)
        self.button6.setText("Drink 6")
        self.button6.move(2*hsize + bsize,  2*vsize+bsize+buf)
        self.button6.clicked.connect(self.button6_clicked)

        # button 7
        self.button7 = QPushButton(w)
        self.button7.setGeometry(0, 0, bsize, bsize)
        self.button7.setText("Drink 7")
        self.button7.move(3*hsize + 2*bsize,  2*vsize+bsize+buf)
        self.button7.clicked.connect(self.button7_clicked)

        # button 8
        self.button8 = QPushButton(w)
        self.button8.setGeometry(0, 0, bsize, bsize)
        self.button8.setText("Drink 8")
        self.button8.move(4*hsize + 3*bsize,  2*vsize+bsize+buf)
        self.button8.clicked.connect(self.button8_clicked)

        layout.addWidget(w)
        self.setLayout(layout)

    def button1_clicked(self):
        print("Button 1 clicked")
        pumpCall(1)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button2_clicked(self):
        print("Button 2 clicked")
        pumpCall(2)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button3_clicked(self):
        print("Button 3 clicked")
        pumpCall(3)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button4_clicked(self):
        print("Button 4 clicked")
        pumpCall(4)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button5_clicked(self):
        print("Button 5 clicked")
        pumpCall(5)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button6_clicked(self):
        print("Button 6 clicked")
        pumpCall(6)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button7_clicked(self):
        print("Button 7 clicked")
        pumpCall(7)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button8_clicked(self):
        print("Button 8 clicked")
        pumpCall(8)
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

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
        # Write a binary 2
        GPIO.output(bit1, False)
        GPIO.output(bit2, True)
        GPIO.output(bit3, False)

        time.sleep(1)

        GPIO.output(bit1, False)
        GPIO.output(bit2, False)
        GPIO.output(bit3, False)
        
    elif flag == 3:
        # Write a binary 3
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
    main()