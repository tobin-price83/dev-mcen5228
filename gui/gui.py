#1024,600

import sys
from random import randint
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

bsize = 200;
hsize = 45;
vsize = 20;
buf = 25;

class MainWindow(QMainWindow):

   def __init__(self):
      app = QApplication(sys.argv)
      app.setStyle("Fusion")

      # Now use a palette to switch to dark colors:
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

      widget = QWidget()

      # BUFFER ROW
      button_exit = QPushButton(widget)
      button_exit.setGeometry(0, 0, 900, 40)
      button_exit.setText("Exit")
      button_exit.move(62, 4*vsize + 2*bsize + buf)
      button_exit.clicked.connect(self.show_approach_window)

      # TOP ROW

      self.button1 = QPushButton(widget)
      self.button1.setGeometry(0, 0, bsize, bsize)
      self.button1.setText("Drink 1")
      self.button1.move(hsize, vsize+buf)
      self.button1.clicked.connect(self.button1_clicked)

      button2 = QPushButton(widget)
      button2.setGeometry( 0, 0, bsize, bsize)
      button2.setText("Drink 2")
      button2.move(2*hsize + bsize, vsize+buf)
      button2.clicked.connect(self.button2_clicked)

      button3 = QPushButton(widget)
      button3.setGeometry(0, 0, bsize, bsize)
      button3.setText("Drink 3")
      button3.move(3*hsize + 2*bsize, vsize+buf)
      button3.clicked.connect(self.button3_clicked)

      button4 = QPushButton(widget)
      button4.setGeometry(0, 0, bsize, bsize)
      button4.setText("Drink 4")
      button4.move(4*hsize + 3*bsize, vsize+buf)
      button4.clicked.connect(self.button4_clicked)

      #  BOTTOM ROW

      button5 = QPushButton(widget)
      button5.setGeometry(0, 0, bsize, bsize)
      button5.setText("Drink 5")
      button5.move(hsize, 2*vsize+bsize+buf)
      button5.clicked.connect(self.button5_clicked)

      button6 = QPushButton(widget)
      button6.setGeometry( 0, 0, bsize, bsize)
      button6.setText("Drink 6")
      button6.move(2*hsize + bsize,  2*vsize+bsize+buf)
      button6.clicked.connect(self.button6_clicked)

      button7 = QPushButton(widget)
      button7.setGeometry(0, 0, bsize, bsize)
      button7.setText("Drink 7")
      button7.move(3*hsize + 2*bsize,  2*vsize+bsize+buf)
      button7.clicked.connect(self.button7_clicked)

      button8 = QPushButton(widget)
      button8.setGeometry(0, 0, bsize, bsize)
      button8.setText("Drink 8")
      button8.move(4*hsize + 3*bsize,  2*vsize+bsize+buf)
      button8.clicked.connect(self.button8_clicked)



      widget.setGeometry(50,50,320,200)
      widget.setWindowTitle("PyQt5 Button Click Example")

      #widget.showMaximized()
      widget.setGeometry(100, 100, 1024, 600)
      widget.show()
      sys.exit(app.exec_())


   def show_approach_window(self, checked):
      if self.w is None:
         self.w = AppraochWindow()
      self.w.show()

   def button1_clicked(self, checked):
      print("Button 1 clicked")

   def button2_clicked():
      print("Button 2 clicked")   

   def button3_clicked():
      print("Button 3 clicked")  

   def button4_clicked():
      print("Button 4 clicked")  

   def button5_clicked():
      print("Button 5 clicked")

   def button6_clicked():
      print("Button 6 clicked")   

   def button7_clicked():
      print("Button 7 clicked")  

   def button8_clicked():
      print("Button 8 clicked") 


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()