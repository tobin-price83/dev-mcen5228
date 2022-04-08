import sys
import time
from random import randint
import Jetson.GPIO as GPIO

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
)

from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

bsize = 200;
hsize = 45;
vsize = 20;
buf = 25;
width = 1024;
height = 600;
startheight = 300;
startwidth = 500;

class MainWindow(QMainWindow):
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
        self.button_start = QPushButton(w)
        self.button_start.setGeometry(0, 0, startwidth, startheight)
        self.button_start.setText("Place Order")
        self.button_start.move(width/2-startwidth/2, height/2 - startheight/2)
        self.button_start.clicked.connect(
            lambda checked: self.button_start_clicked()
        )
        self.button_start.show()

        ### SCAN MENU ### --------------------------------------------------------------------------------------------
        self.button_scan = QPushButton(w)
        self.button_scan.setGeometry(0, 0, 900, 40)
        self.button_scan.setText("Scan ID")
        self.button_scan.move(62, 4*vsize + 2*bsize + buf - 60)
        self.button_scan.clicked.connect(
            lambda checked: self.button_scan_clicked()
        )
        self.button_scan.hide()

        self.button_exit = QPushButton(w)
        self.button_exit.setGeometry(0, 0, 900, 40)
        self.button_exit.setText("Cancel Order")
        self.button_exit.move(62, 4*vsize + 2*bsize + buf)
        self.button_exit.clicked.connect(
            lambda checked: self.button_exit_clicked()
        )
        self.button_exit.hide()

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
        self.button1.hide()

        self.button2 = QPushButton(w)
        self.button2.setGeometry( 0, 0, bsize, bsize)
        self.button2.setText("Drink 2")
        self.button2.move(2*hsize + bsize, vsize+buf)
        self.button2.clicked.connect(
            lambda checked: self.button2_clicked()
        )
        self.button2.hide()

        self.button3 = QPushButton(w)
        self.button3.setGeometry(0, 0, bsize, bsize)
        self.button3.setText("Drink 3")
        self.button3.move(3*hsize + 2*bsize, vsize+buf)
        self.button3.clicked.connect(
            lambda checked: self.button3_clicked()
        )
        self.button3.hide()

        self.button4 = QPushButton(w)
        self.button4.setGeometry(0, 0, bsize, bsize)
        self.button4.setText("Drink 4")
        self.button4.move(4*hsize + 3*bsize, vsize+buf)
        self.button4.clicked.connect(
            lambda checked: self.button4_clicked()
        )
        self.button4.hide()

        #  BOTTOM ROW

        self.button5 = QPushButton(w)
        self.button5.setGeometry(0, 0, bsize, bsize)
        self.button5.setText("Drink 5")
        self.button5.move(hsize, 2*vsize+bsize+buf)
        self.button5.clicked.connect(
            lambda checked: self.button5_clicked()
        )
        self.button5.hide()

        self.button6 = QPushButton(w)
        self.button6.setGeometry( 0, 0, bsize, bsize)
        self.button6.setText("Drink 6")
        self.button6.move(2*hsize + bsize,  2*vsize+bsize+buf)
        self.button6.clicked.connect(
            lambda checked: self.button6_clicked()
        )
        self.button6.hide()

        self.button7 = QPushButton(w)
        self.button7.setGeometry(0, 0, bsize, bsize)
        self.button7.setText("Drink 7")
        self.button7.move(3*hsize + 2*bsize,  2*vsize+bsize+buf)
        self.button7.clicked.connect(
            lambda checked: self.button7_clicked()
        )
        self.button7.hide()

        self.button8 = QPushButton(w)
        self.button8.setGeometry(0, 0, bsize, bsize)
        self.button8.setText("Drink 8")
        self.button8.move(4*hsize + 3*bsize,  2*vsize+bsize+buf)
        self.button8.clicked.connect(
            lambda checked: self.button8_clicked()
        )
        self.button8.hide()
    

        # w.setLayout(l)
        
        self.setCentralWidget(w)
        
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
        self.button_start.hide()
        self.button_scan.show()
        self.button_exit.show()

    def button_scan_clicked(self):
        self.button_scan.hide()
        self.show_all_buttons()

    def button_exit_clicked(self):
        self.hide_all_buttons()
        self.button_exit.hide()
        self.button_start.show()
        print("Exit Button Pushed")

    def button1_clicked(self):
        self.hide_all_buttons()
        print("Button 1 clicked")
        time.sleep(1)
        pumpCall(1) # Call func
        self.button_start.show()
        self.button_exit.hide()

    def button2_clicked(self):
        self.hide_all_buttons()
        print("Button 2 clicked")   
        time.sleep(1)
        pumpCall(2) # Call func
        self.button_start.show()
        self.button_exit.hide()

    def button3_clicked(self):
        self.hide_all_buttons()
        print("Button 3 clicked")  
        time.sleep(1)
        pumpCall(3)
        self.button_start.show()
        self.button_exit.hide()

    def button4_clicked(self):
        self.hide_all_buttons()
        print("Button 4 clicked")  
        time.sleep(1)
        pumpCall(4)
        self.button_start.show()
        self.button_exit.hide()

    def button5_clicked(self):
        self.hide_all_buttons()
        print("Button 5 clicked")
        time.sleep(1)
        pumpCall(5)
        self.button_start.show()
        self.button_exit.hide()

    def button6_clicked(self):
        self.hide_all_buttons()
        print("Button 6 clicked")   
        time.sleep(1)
        pumpCall(6)
        self.button_start.show()
        self.button_exit.hide()

    def button7_clicked(self):
        self.hide_all_buttons()
        print("Button 7 clicked")  
        time.sleep(1)
        pumpCall(7)
        self.button_start.show()
        self.button_exit.hide()

    def button8_clicked(self):
        self.hide_all_buttons()
        print("Button 8 clicked")
        time.sleep(1)
        pumpCall(8)
        self.button_start.show()
        self.button_exit.hide()

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

app = QApplication(sys.argv)
#palette = QPalette()
#palette.setColor(QPalette.Window, QColor(53, 53, 53))
#palette.setColor(QPalette.WindowText, Qt.white)
#palette.setColor(QPalette.Base, QColor(25, 25, 25))
#palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
#palette.setColor(QPalette.ToolTipBase, Qt.black)
#palette.setColor(QPalette.ToolTipText, Qt.white)
#palette.setColor(QPalette.Text, Qt.white)
#palette.setColor(QPalette.Button, QColor(53, 53, 53))
#palette.setColor(QPalette.ButtonText, Qt.white)
#palette.setColor(QPalette.BrightText, Qt.red)
#palette.setColor(QPalette.Link, QColor(42, 130, 218))
#palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
#palette.setColor(QPalette.HighlightedText, Qt.black)
#app.setPalette(palette)

w = MainWindow()
w.setGeometry(100, 100, 1024, 600)
w.show()
app.exec()




