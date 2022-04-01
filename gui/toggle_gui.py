#1024,600

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

bsize = 200;
hsize = 45;
vsize = 20;
buf = 25;

class AppraochWindow(QWidget):
   def __init__(self):
      super().__init__()
      layout = QVBoxLayout()
      self.label = QLabel("Another Window % d" % randint(0,100))
      layout.addWidget(self.label)
      self.setLayout(layout)

class MainWindow(QWidget):

   def __init__(self):
      super().__init__()
      self.w = None

      self.button1 = QPushButton("Drink")
      self.button1.setGeometry(0, 0, 200, 200)
      self.button1.setText("Drink 1")
      self.button1.move(0,0)
      self.button1.clicked.connect(self.button1_clicked)


    #   widget.setGeometry(50,50,320,200)
    #   widget.setWindowTitle("PyQt5 Button Click Example")

      #widget.showMaximized()
    #   widget.setGeometry(100, 100, 1024, 600)
    #   widget.show()
    #   sys.exit(app.exec_())


   def show_approach_window(self, checked):
      if self.w is None:
         self.w = AppraochWindow()
      self.w.show()

   def button1_clicked(self, checked):
      print("Button 1 clicked")


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()