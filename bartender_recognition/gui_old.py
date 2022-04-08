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
)

from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, Qt

bsize = 200;
hsize = 45;
vsize = 20;
buf = 25;
width = 1024;
height = 600;
startheight = 300;
startwidth = 500;

class CaptureVideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    vid_rec = video_recognition.VideoRecognition()

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # vid_rec = video_recognition.VideoRecognition()
        # capture from rpi camera
        cap = cv2.VideoCapture(video_recognition.gstreamer_pipeline(flip_method=2),cv2.CAP_GSTREAMER)

        process_this_frame = True

        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                if process_this_frame:
                    preview_frame = vid_rec.find_faces(cv_img)
                process_this_frame = not process_this_frame
                preview_frame = vid_rec.preview_frame(cv_img)
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        approach_widget = approachWidget(self)
        appraoch_widget.button.clicked.connect(self.)


class MainWindowOld(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.window1 = Window()
        l = QVBoxLayout()
        w = QWidget()
        self.setStyleSheet('QWidget {font: "Roboto Mono"}')

        # l = QVBoxLayout()
        # self.button1 = QPushButton("Push for Window 1")
        # self.button1.clicked.connect(
        #     lambda checked: self.toggle_window()
        # )
        # l.addWidget(self.button1)

        ### APPROACH MENU ### --------------------------------------------------------------------------------------------

        # approach menu button
        self.button_start = QPushButton(self)
        self.button_start.setGeometry(0, 0, startwidth, startheight)
        self.button_start.setText("Place Order")
        self.button_start.move(width/2-startwidth/2, height/2 - startheight/2)
        self.button_start.clicked.connect(
            lambda checked: self.button_start_clicked()
        )
        # self.button_start.show()

        # create layout and add widgets
        approach_menu = QVBoxLayout()
        approach_menu.addWidget(self.button_start)
        # self.setLayout(approach_menu)

        ### SCAN MENU ### --------------------------------------------------------------------------------------------
        # video feed preview
        self.video_feed = QLabel(self)
        self.video_feed.resize(640,360)


        self.button_scan = QPushButton(w)
        self.button_scan.setGeometry(0, 0, 900, 40)
        self.button_scan.setText("Scan ID")
        self.button_scan.move(62, 4*vsize + 2*bsize + buf - 60)
        self.button_scan.clicked.connect(
            lambda checked: self.button_scan_clicked()
        )
        # self.button_scan.hide()

        self.button_exit = QPushButton(w)
        self.button_exit.setGeometry(0, 0, 900, 40)
        self.button_exit.setText("Cancel Order")
        self.button_exit.move(62, 4*vsize + 2*bsize + buf)
        self.button_exit.clicked.connect(
            lambda checked: self.button_exit_clicked()
        )

        # add widgets to scan menu
        scan_menu = QVBoxLayout()
        scan_menu.addWidget(self.video_feed)
        scan_menu.addWidget(self.button_scan)
        scan_menu.addWidget(self.button_exit)

        # self.button_exit.hide()

        # self.id_image = QPixmap('./id_image.jpeg')
        # self.move(100, 100)
        # self.id_image.show()

        # self.pic = QLabel(self)
        # self.pic.setPixmap(QPixmap("./id_image.jpg"))
        # self.pic.move(100, 100)
        # self.pic.show()

        # label.setPixmap(pixmap)
        # self.resize(id_image.width(),i.height())

        ### ORDERING MENU ### --------------------------------------------------------------------------------------------
        
        self.button1 = QPushButton(w)
        self.button1.setGeometry(0, 0, bsize, bsize)
        self.button1.setText("Drink 1")
        self.button1.move(hsize, vsize+buf)
        self.button1.clicked.connect(
            lambda checked: self.button1_clicked()
        )
        # self.button1.hide()

        self.button2 = QPushButton(w)
        self.button2.setGeometry( 0, 0, bsize, bsize)
        self.button2.setText("Drink 2")
        self.button2.move(2*hsize + bsize, vsize+buf)
        self.button2.clicked.connect(
            lambda checked: self.button2_clicked()
        )
        # self.button2.hide()

        self.button3 = QPushButton(w)
        self.button3.setGeometry(0, 0, bsize, bsize)
        self.button3.setText("Drink 3")
        self.button3.move(3*hsize + 2*bsize, vsize+buf)
        self.button3.clicked.connect(
            lambda checked: self.button3_clicked()
        )
        # self.button3.hide()

        self.button4 = QPushButton(w)
        self.button4.setGeometry(0, 0, bsize, bsize)
        self.button4.setText("Drink 4")
        self.button4.move(4*hsize + 3*bsize, vsize+buf)
        self.button4.clicked.connect(
            lambda checked: self.button4_clicked()
        )
        # self.button4.hide()

        #  BOTTOM ROW

        self.button5 = QPushButton(w)
        self.button5.setGeometry(0, 0, bsize, bsize)
        self.button5.setText("Drink 5")
        self.button5.move(hsize, 2*vsize+bsize+buf)
        self.button5.clicked.connect(
            lambda checked: self.button5_clicked()
        )
        # self.button5.hide()

        self.button6 = QPushButton(w)
        self.button6.setGeometry( 0, 0, bsize, bsize)
        self.button6.setText("Drink 6")
        self.button6.move(2*hsize + bsize,  2*vsize+bsize+buf)
        self.button6.clicked.connect(
            lambda checked: self.button6_clicked()
        )
        # self.button6.hide()

        self.button7 = QPushButton(w)
        self.button7.setGeometry(0, 0, bsize, bsize)
        self.button7.setText("Drink 7")
        self.button7.move(3*hsize + 2*bsize,  2*vsize+bsize+buf)
        self.button7.clicked.connect(
            lambda checked: self.button7_clicked()
        )
        # self.button7.hide()

        self.button8 = QPushButton(w)
        self.button8.setGeometry(0, 0, bsize, bsize)
        self.button8.setText("Drink 8")
        self.button8.move(4*hsize + 3*bsize,  2*vsize+bsize+buf)
        self.button8.clicked.connect(
            lambda checked: self.button8_clicked()
        )
        # self.button8.hide()
    
        # add to order menu layout
        order_menu = QVBoxLayout()
        order_menu.addWidget(self.button1)
        order_menu.addWidget(self.button2)
        order_menu.addWidget(self.button3)
        order_menu.addWidget(self.button4)
        order_menu.addWidget(self.button5)
        order_menu.addWidget(self.button6)
        order_menu.addWidget(self.button7)
        order_menu.addWidget(self.button8)

        # w.setLayout(l)
        
        # self.setCentralWidget(w)

        # show starting screen
        self.setLayout(approach_menu)
        
    def hide_all_buttons(self):
        self.button1.hide()
        self.button2.hide() 
        self.button3.hide() 
        self.button4.hide() 
        self.button5.hide() 
        self.button6.hide() 
        self.button7.hide() 
        self.button8.hide() 
        self.button_scan.hide()

    def show_all_buttons(self):
        self.button1.show()
        self.button2.show() 
        self.button3.show() 
        self.button4.show() 
        self.button5.show() 
        self.button6.show() 
        self.button7.show() 
        self.button8.show() 

    def button_start_clicked(self):
        # self.button_start.hide()
        # self.button_scan.show()
        # self.button_exit.show()
        self.setLayout(scan_menu)
        self.thread.start()

    def button_scan_clicked(self):
        # self.thread = VideoThread()
        # self.thread.change_pixmap_signal.connect(self.update_image)
        # self.thread.start()
        # self.button_scan.hide()
        # self.show_all_buttons()

        # take photo and train
        self.setLayout(order_menu)
        self.thread.stop()

    def button_exit_clicked(self):
        # self.hide_all_buttons()
        # self.button_exit.hide()
        # self.button_start.show()
        print("Exit Button Pushed")
        self.setLayout(approach_menu)

    def button1_clicked(self):
        self.hide_all_buttons()
        print("Button 1 clicked")
        time.sleep(1)
        # self.button_start.show()
        # self.button_exit.hide()
        self.setLayout(approach_menu)

    def button2_clicked(self):
        self.hide_all_buttons()
        print("Button 2 clicked")   
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()

    def button3_clicked(self):
        self.hide_all_buttons()
        print("Button 3 clicked")  
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()

    def button4_clicked(self):
        self.hide_all_buttons()
        print("Button 4 clicked")  
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()

    def button5_clicked(self):
        self.hide_all_buttons()
        print("Button 5 clicked")
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()

    def button6_clicked(self):
        self.hide_all_buttons()
        print("Button 6 clicked")   
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()

    def button7_clicked(self):
        self.hide_all_buttons()
        print("Button 7 clicked")  
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()

    def button8_clicked(self):
        self.hide_all_buttons()
        print("Button 8 clicked")
        time.sleep(1)
        self.button_start.show()
        self.button_exit.hide()


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class ApproachWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AproachWidget, self).__init__(parent)
        layout = QVHoxLayout()
        self.button = QPushButton('Place Order')
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.click.connect(self.parent())

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
    w.show()
    app.exec()

if __name__ == '__main__':
    make_gui()