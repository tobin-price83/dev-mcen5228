import sys
import time

from random import randint
import video_recognition
import video_pipeline
import cv2
import numpy as np
import Jetson.GPIO as GPIO

# from gi.repository import GObject, Gst, GstVideo  

# Set up GPIO
GPIO.setmode(GPIO.BOARD) # Other options are BCM, CVM, and TEGRA_SOC

bit1 = 36
bit2 = 38
bit3 = 40

GPIO.setup(bit1, GPIO.OUT)
GPIO.setup(bit2, GPIO.OUT)
GPIO.setup(bit3, GPIO.OUT)


from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QStackedLayout,
)

from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont, QImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, Qt
from PyQt5 import QtCore, QtGui

bsize = 200;
hsize = 45;
vsize = 20;
buf = 25;
width = 1024;
height = 600;
startheight = 300;
startwidth = 500;

class GSTThread(QThread):
    # ImageUpdate = pyqtSignal(QImage)
    ImageUpdate = pyqtSignal(QPixmap)
    vid_rec = video_recognition.VideoRecognition()

    def __init__(self, Parent=None):
        super().__init__()
        self._run_flag = True
        self._preview_flag = False

        # placeholder pixmap
        p = QPixmap(640,360)
        p.fill(QColor('darkRed'))
        self.ImageUpdate.emit(p)
        
    def video_preview(self):
        print("Running video_preview")
        # flag preview thread as running
        self._preview_flag = True
        print("_preview_flag:",self._preview_flag)

        # start capture feed
        print("Starting capture")
        gst_string = video_pipeline.gstreamer_pipeline(flip_method=2,frameskip=15)
        print(gst_string)
        self.cap = cv2.VideoCapture(gst_string,cv2.CAP_GSTREAMER)

        # read frame buffer while idle, but don't display
        while self._preview_flag:
            ret, frame = self.cap.read()
            # print("Reading frame")
            if ret:
                # if not self._preview_flag:
                #     break
                # self.change_pixmap_signal.emit(cv_img)
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = Image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QtGui.QImage(Image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                p = convert_to_Qt_format.scaled(640, 360, Qt.KeepAspectRatio)
                # emit QPixmap signal
                # print("Emitting pixmap")
                self.ImageUpdate.emit(QPixmap.fromImage(p))
        # self.cap.release()

    def stop(self):
        self._preview_flag = False
        print("_preview_flag:",self._preview_flag)
        self.wait()

    def shutdown(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self._preview_flag = False
        # shut down capture system
        self.cap.release()
        # self.wait()
        self.quit()
        


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

        # create video thread in top-level context
        self.video_thread = GSTThread()
        # connect to image update
        # self.video_thread.change_pixmap_signal.connect(self.update_image)

        # create and connect window navigation
        # approach window
        approach_widget = ApproachWidget(self)
        approach_widget.button.clicked.connect(self.scan_window)
        self.stackedLayout.addWidget(approach_widget)
        # scan window
        scan_widget = ScanWidget(self)
        scan_widget.scan_button.clicked.connect(self.order_window)
        scan_widget.exit_button.clicked.connect(self.approach_window)
        # scan_widget.video
        # scan_widget.video_thread.
        self.stackedLayout.addWidget(scan_widget)
        # order window
        order_widget = OrderWidget(self)
        self.stackedLayout.addWidget(order_widget)

        
        # make stacked layout central widget
        layout.addLayout(self.stackedLayout)

        # run video preview thread after all layouts are ready
        # self.video_thread.video_preview()
        # print("Video preview running")


    def approach_window(self):
        print("Opening approach menu")
        self.stackedLayout.setCurrentIndex(0)
        QApplication.processEvents()

    def scan_window(self):
        print("Opening scan menu")
        
        self.stackedLayout.setCurrentIndex(1)
        # time.sleep(3)
        QApplication.processEvents()
        self.video_thread.video_preview()        
        # QApplication.processEvents()
        # self.layout.stackedLayout.scan_widget.video_feed(self)

    def order_window(self):
        print("Opening order menu")
        self.stackedLayout.setCurrentIndex(2)
        QApplication.processEvents()

    def closeEvent(self, event):
        self.video_thread.shutdown()
        event.accept()


class ApproachWidget(QWidget):
    def __init__(self, parent=None):
        super(ApproachWidget, self).__init__(parent)
        w = QWidget()
        self.button = QPushButton(w)
        self.button.setFont(QFont('Arial',24))
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
        layout = QVBoxLayout()
        w = QWidget()
        
        # placeholder pixmap
        p = QPixmap(640,360)
        p.fill(QColor('darkRed'))
        # self.ImageUpdate.emit(p)

        # initialize video preview window
        self.video_feed = QLabel(w)
        # self.video_feed = QLabel(self)
        self.video_feed.setGeometry(0,0,640,360)
        self.video_feed.setPixmap(p)

        # scan button
        self.scan_button = QPushButton(w)
        self.scan_button.setFont(QFont('Arial',16))
        self.scan_button.setText("Scan ID")
        self.scan_button.setGeometry(0,0,900,40)
        self.scan_button.move(62, 4*vsize + 2*bsize + buf - 72)
        self.scan_button.clicked.connect(self.scan_function)

        # exit button
        self.exit_button = QPushButton(w)
        self.exit_button.setFont(QFont('Arial',16))
        self.exit_button.setText("Exit")
        self.exit_button.setGeometry(0,0,900,40)
        self.exit_button.move(62, 4*vsize + 2*bsize + buf-20)
        self.exit_button.clicked.connect(self.exit_function)

        layout.addWidget(w)
        # layout.addWidget(self.video_feed)
        self.setLayout(layout)

        # connect parent level video_thread to image update
        self.parent().video_thread.ImageUpdate.connect(self.update_image)

    def scan_function(self):
        print("Scan ID clicked")
        print("Stopping video preview")
        # self.parent().video_thread.stop()
        # self.parent().video_thread.stop()
        self.parent().video_thread.shutdown()
        # time.sleep(5)
        self.parent().video_thread.wait()
        self.parent().order_window()
        

    def exit_function(self):
        print("Exit button clicked")
        print("Stopping video preview")
        # self.parent().video_thread.stop()
        self.parent().video_thread.shutdown()
        self.parent().video_thread.wait()
        self.parent().approach_window()

    @pyqtSlot(QPixmap)
    def update_image(self, Image):
        if self.parent().video_thread._preview_flag:
            self.video_feed.setPixmap(Image)
            QApplication.processEvents()


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


def make_gui():
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    w = MainWindow()
    w.setGeometry(100, 100, 1024, 600)
    # w.setGeometry(100, 100, 720, 480)
    w.show()
    app.exec()

if __name__ == '__main__':
    make_gui()