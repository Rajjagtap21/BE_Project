import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from PyQt5.QtGui import QPixmap
from capgenerator import generate_caption 
import pyttsx3
import time
from win32api import GetSystemMetrics
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

global d
global st
global radiobutton
global cnt
st="on"
cnt=0
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(GetSystemMetrics(0), GetSystemMetrics(1)))    
        self.setWindowTitle("Image Captioning") 
        
        oImage = QImage("G:/BE project/ImageCapGen/assets/bg1.jpg")
        sImage = oImage.scaled(QSize(GetSystemMetrics(0),GetSystemMetrics(1)))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage)) 
        self.setPalette(palette)
		
        self.pybutton = QPushButton(self)
        self.pybutton.setFont(QFont('Comic Sans MS', 15))
        self.pybutton.clicked.connect(self.clickMethod)
        self.pybutton.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/sicon2.png'))
        self.pybutton.setStyleSheet("background-color:white")
        self.pybutton.setIconSize(QtCore.QSize(150,50))
        self.pybutton.resize(150,50)
        self.pybutton.move(885, 115) 
		
        extbtn = QPushButton(self)
        extbtn.setFont(QFont('Comic Sans MS', 15))
        extbtn.clicked.connect(self.exitui)
        extbtn.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/exicon.png'))
        extbtn.setStyleSheet("background-color:rgb(51,153,255)")
        extbtn.setIconSize(QtCore.QSize(50,50))
        extbtn.resize(50,50)
        extbtn.move(15, 15) 
		
        self.setbtn = QPushButton(self)
        self.setbtn.setFont(QFont('Comic Sans MS', 15))
        self.setbtn.clicked.connect(self.voice)
        #self.setbtn.clicked.connect(self.setd)
        self.setbtn.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/son3.png'))
        self.setbtn.setStyleSheet("background-color:rgb(51,153,255)")
        self.setbtn.setIconSize(QtCore.QSize(50,50))
        self.setbtn.resize(50,50)
        self.setbtn.move(1850, 15)
		
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Impact', 18))
        self.label.setStyleSheet("QLabel {background-color: white;}")
        self.label.move(350,220)
        self.label.resize(1200,50)
		
        self.img1 = QLabel(self)
        self.img1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img1.setAlignment(Qt.AlignCenter)
        self.img1.setFont(QFont('Comic Sans MS', 15))
        #self.img1.setStyleSheet("QLabel {background-color: yellow;}")
        self.img1.move(20,280)
        self.img1.resize(950,800)
		
        self.img2 = QLabel(self)
        self.img2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img2.setAlignment(Qt.AlignCenter)
        self.img2.setFont(QFont('Comic Sans MS', 15))
        #self.img2.setStyleSheet("QLabel {background-color: yellow;}")
        self.img2.move(960,270)
        self.img2.resize(950,800)
		
        self.show()
   	
    def voice(self):
        global st	
        global cnt
        cnt=cnt+1
        if(cnt % 2 == 0):
          st='on'
          self.setbtn.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/son3.png'))
        else:
          st='off'
          self.setbtn.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/soff3.png'))
 
    def exitui(self, event):
        reply = QMessageBox.question(
            self, "Exit?",
            "Are you sure you want to Exit?",
            QMessageBox.Yes | QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            self.close()
			
    def setd(self):

         global d
         global radiobutton
         global st
         d = QDialog()
         layout = QGridLayout()
         d.setLayout(layout)
         radiobutton = QRadioButton()
         #radiobutton.setChecked(True)
         radiobutton.state = "on"
         radiobutton.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/son3.png'))
         radiobutton.toggled.connect(self.onClicked)
         layout.addWidget(radiobutton, 0, 0)
         radiobutton.setFont(QFont('Comic Sans MS', 15))
         radiobutton.setIconSize(QtCore.QSize(45,45))
		 
         radiobutton = QRadioButton()
         radiobutton.state = "off"
         radiobutton.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/soff3.png'))
         
         radiobutton.toggled.connect(self.onClicked)
         layout.addWidget(radiobutton, 0, 1)
		 
         radiobutton.setFont(QFont('Comic Sans MS', 15))
         radiobutton.setIconSize(QtCore.QSize(45,45))
		 
         d.setWindowTitle("Sound")
         d.setGeometry(1000,100,200,100)
         d.setWindowModality(Qt.ApplicationModal)
         d.exec_()
			
         		 
    def onClicked(self):
       
        global st
        global radiobutton
        global d
        rb=d.sender()
        if(rb.state == 'on'):
          st='on'
          self.setbtn.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/son3.png'))
        elif(rb.state == 'off'):
          st='off'
          self.setbtn.setIcon(QtGui.QIcon('G:/BE project/ImageCapGen/assets/soff3.png'))
        		
        d.close()			


    def clickMethod(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', './test' , 'Image files (*.jpg *.png *.jpeg)')
        imagePath = fname[0]
        op=""
        global st
        if(imagePath==""):
           if(self.label.text()==""):
              self.label.setText("Please Select An Image File")
        else:
           cp=generate_caption.getcap(imagePath)
           f= open("./output/cap.txt","w+")
           for w in cp:
                 f.write(w)
                 f.write(' ')
           f.close()
            
           with open("./output/cap.txt") as f1:
                caps = f1.readlines()
           for ele in caps:
                op += ele
         
           self.label.setText(op+'.')
           pixmap = QPixmap(imagePath)
           pm = pixmap.scaled(650, 500, QtCore.Qt.KeepAspectRatio)
           self.img1.setPixmap(QPixmap(pm))
           pixmap1 = QPixmap('./output/1.png')
           self.img2.setPixmap(QPixmap(pixmap1))
		   
           if(st=='on'):
              engine = pyttsx3.init()
              engine.setProperty('rate', 140)
              #time.sleep(20)
              engine.say(caps)
              engine.runAndWait()
              engine.stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    #mainWin.show()
    sys.exit( app.exec_() )