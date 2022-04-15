import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class Thread(QThread):
    print("QThread Initiating...")
    changePixmap = pyqtSignal(QImage)
    print("PixMap Created...")

    def run(self):
        # cap = cv2.VideoCapture(0)
        print("Video Capture Initiated")
        cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2160, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)
        while True:
            print("Yo")
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            else:
                print("Error")


class App(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        print("Initiation Pixmap setImage...")
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.title = "Ryan's Fantastic No Good But Very Fun App"
        self.left = 50
        self.top = 50
        self.width = 500
        self.height= 500

        print("Initiating UI");
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

app = QApplication(sys.argv)
w = App()

w.setGeometry(100, 100, 1024, 600)
# w.setGeometry(100, 100, 720, 480)
w.show()
# app.setUI()
app.exec()