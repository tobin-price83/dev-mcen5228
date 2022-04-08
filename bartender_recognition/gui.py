import sys
import time
from random import randint
import video_recognition
import cv2
import numpy as np


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
    # changePixmap = pyqtSignal(QImage)
    change_pixmap_signal = pyqtSignal(np.ndarray)
    vid_rec = video_recognition.VideoRecognition()

    cap = cv2.VideoCapture(video_recognition.gstreamer_pipeline(flip_method=2),cv2.CAP_GSTREAMER)

    def __init__(self, Parent=None):
        super().__init__()
        self._run_flag = True
        self._preview_flag = False

        # start capture feed
        # print("Starting capture")
        # # self.cap = 
        
    def video_preview(self):
        # flag preview thread as running
        self._preview_flag = True

        print("Running video_preview")

        # capture from CSI camera
        while self._preview_flag:
            ret, cv_img = self.cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        # cap.release()

    # def start_v4l(self):
    #     # flag thread as running
    #     self._run_flag = True

    #     # capture from webcam
    #     cap = cv2.VideoCapture(video_recognition.v4l_pipeline(),cv2.CAP_GSTREAMER)
    #     while self._run_flag:
    #         ret, cv_img = cap.read()
    #         if ret:
    #             rgbImage = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    #             h, w, ch = rgbImage.shape
    #             bytesPerLine = ch * w
    #             convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
    #             p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
    #             self.changePixmap.emit(p)
    #             # self.change_pixmap_signal.emit(cv_img)
    #     # shut down capture system
    #     cap.release()

    # def face_capture(self):
    #     # vid_rec = video_recognition.VideoRecognition()
    #     # capture from rpi camera
    #     cap = cv2.VideoCapture(video_recognition.gstreamer_pipeline(flip_method=2),cv2.CAP_GSTREAMER)

    #     process_this_frame = True

    #     while self._run_flag:
    #         ret, cv_img = cap.read()
    #         if ret:
    #             if process_this_frame:
    #                 preview_frame = vid_rec.find_faces(cv_img)
    #             process_this_frame = not process_this_frame
    #             preview_frame = vid_rec.preview_frame(cv_img)
    #             self.change_pixmap_signal.emit(cv_img)
    #     # shut down capture system
    #     cap.release()

    def stop(self):
        self._preview_flag = False

    def shutdown(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
        # shut down capture system
        self.cap.release()



# class VideoThread(QThread):
#     change_pixmap_signal = pyqtSignal(np.ndarray)

#     def __init__(self):
#         super().__init__()
#         self._run_flag = True

#     def run(self):
#         # capture from web cam
#         cap = cv2.VideoCapture(0)
#         while self._run_flag:
#             ret, cv_img = cap.read()
#             if ret:
#                 self.change_pixmap_signal.emit(cv_img)
#         # shut down capture system
#         cap.release()

#     def stop(self):
#         """Sets run flag to False and waits for thread to finish"""
#         self._run_flag = False
#         self.wait()

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

        # create video thread
        # self.thread = GSTThread()

        # create and connect window navigation
        # approach window
        approach_widget = ApproachWidget(self)
        approach_widget.button.clicked.connect(self.scan_window)
        self.stackedLayout.addWidget(approach_widget)
        # scan window
        scan_widget = ScanWidget(self)
        scan_widget.scan_button.clicked.connect(self.order_window)
        scan_widget.exit_button.clicked.connect(self.approach_window)
        # scan_widget.video_thread.
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
        self.stackedLayout.setCurrentIndex(1)
        # self.thread.video_preview()
        # self.layout.stackedLayout.scan_widget.video_feed(self)

    def order_window(self):
        print("Opening order menu")
        self.stackedLayout.setCurrentIndex(2)

    # def start_gst(self):
    #     print("Starting gst feed")
    #     self.thread.start_gst()

    # def update_image(self):
    #     self.


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
        
        # initialize video preview window
        self.video_feed = QLabel(w)
        self.video_feed.setGeometry(0,0,640,480)
        video_thread = GSTThread()
        # video_thread = self.parent().thread
        video_thread.change_pixmap_signal.connect(self.update_image)

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

        video_thread.video_preview()

    def video_feed(self):
        print("Called video_feed")
        # start video thread
        video_thread.video_preview()

    def scan_function(self):
        print("Scan ID clicked")
        print("Stopping video preview")
        video_thread.stop()
        self.parent().order_window()

    def exit_function(self):
        print("Exit button clicked")
        print("Stopping video preview")
        video_thread.stop()
        self.parent().approach_window()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        # self.video_feed.setPixmap(QPixmap.fromImage(image))
        qt_img = self.convert_cv_qt(cv_img)
        self.video_feed.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

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
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button2_clicked(self):
        print("Button 2 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button3_clicked(self):
        print("Button 3 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button4_clicked(self):
        print("Button 4 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button5_clicked(self):
        print("Button 5 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button6_clicked(self):
        print("Button 6 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button7_clicked(self):
        print("Button 7 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()

    def button8_clicked(self):
        print("Button 8 clicked")
        # return to approach menu
        time.sleep(1)
        self.parent().approach_window()


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