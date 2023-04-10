import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from soft import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtGui
import numpy
from detect import infer
import os
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor
import cv2
from PyQt5.QtWidgets import QDial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize
from QCandyUi import CandyWindow


path = os.getcwd()
def QImage2CV(qimg):
    
    tmp = qimg
    
    #使用numpy创建空的图象
    cv_image = numpy.zeros((tmp.height(), tmp.width(), 3), dtype=numpy.uint8)
    
    for row in range(0, tmp.height()):
        for col in range(0,tmp.width()):
            r = qRed(tmp.pixel(col, row))
            g = qGreen(tmp.pixel(col, row))
            b = qBlue(tmp.pixel(col, row))
            cv_image[row,col,0] = b
            cv_image[row,col,1] = g
            cv_image[row,col,2] = r
    
    return cv_image
def CV2QImage(cv_image):
    
    width = cv_image.shape[1] #获取图片宽度
    height = cv_image.shape[0]  #获取图片高度
    
    pixmap = QPixmap(width, height) #根据已知的高度和宽度新建一个空的QPixmap,
    qimg = pixmap.toImage()  #将pximap转换为QImage类型的qimg
    
    #循环读取cv_image的每个像素的r,g,b值，构成qRgb对象，再设置为qimg内指定位置的像素
    for row in range(0, height):
        for col in range(0,width):
            b = cv_image[row,col,0]
            g = cv_image[row,col,1]
            r = cv_image[row,col,2]
            
            pix = qRgb(r, g, b)
            qimg.setPixel(col, row, pix)
    
    return qimg #转换完成，返回
def CV2grayQImage(cv_image):
    
    width = cv_image.shape[1] #获取图片宽度
    height = cv_image.shape[0]  #获取图片高度
    
    pixmap = QPixmap(width, height) #根据已知的高度和宽度新建一个空的QPixmap,
    qimg = pixmap.toImage()  #将pximap转换为QImage类型的qimg
    
    #循环读取cv_image的每个像素的r,g,b值，构成qRgb对象，再设置为qimg内指定位置的像素
    for row in range(0, height):
        for col in range(0,width):
            b = cv_image[row,col]
            g = cv_image[row,col]
            r = cv_image[row,col]
            
            pix = qRgb(r, g, b)
            qimg.setPixel(col, row, pix)
    
    return qimg #转换完成，返回

def calculate(self):
    global i,j,k,l
    Confidence=numpy.array([                  
	[ [ [ 88, 94, 95, 92],
    [ 85, 88, 88, 89 ],
	[ 82, 88, 88, 87 ],
	[ 79, 84, 82, 74 ],
	[ 88, 88, 88, 88 ] ],
	[[ 88, 91, 81, 89 ],
     [ 92, 93, 93, 92 ],
	[ 85, 88, 90, 88 ],
	[ 92, 93, 94, 93 ],
	[ 88, 88, 88, 88 ] ],
	[ [ 79, 82, 92, 96 ],
    [ 95, 96, 98, 96 ],
	[ 81, 85, 86, 82 ],
	[ 69, 75, 81, 86 ],
	[ 88, 88, 88, 88 ] ] ],
	[ 
	[ [ 97, 98, 98, 96 ],
    [ 84, 85, 86, 85 ],
	[ 88, 90, 91, 90 ],
	[ 86, 89, 90, 89 ],
	[ 88, 88, 88, 88 ] ],
	[ [ 98, 97, 86, 94 ],
    [ 95, 96, 95, 92 ],
	[ 97, 97, 97, 96 ],
	[ 97, 97, 98, 99 ],
	[ 88, 88, 88, 88 ] ],
	[[ 85, 94, 95, 95 ],
     [ 100, 100, 100, 99 ],
	[ 75, 76, 75, 68 ],
	[ 83, 85, 86, 86 ],
	[ 88, 88, 88, 88 ] ] ],
	[ 
	[ [ 97, 98, 99, 98 ],
    [ 88, 86, 87, 87 ],
	[ 88, 92, 94, 93 ],
	[ 88, 93, 93, 91 ],
	[ 88, 88, 88, 88 ] ],
	[ [ 97, 98, 89, 96 ],
    [ 97, 97, 97, 95 ]
	[ 95, 98, 98, 98 ],
	[ 98, 99, 99, 99 ],
	[ 88, 88, 88, 88 ] ],
	[ [ 93, 95, 97, 97 ],
    [ 100, 100, 100, 100 ],
	[ 92, 92, 93, 92 ],
	[ 86, 89, 89, 92 ],
	[ 88, 88, 88, 88 ] ] ],
    [ 
	[[ 94, 97, 97, 93 ],
     [ 90, 88, 88, 89 ],
	[ 87, 88, 88, 88 ],
	[ 87, 84, 83, 79 ],
	[ 88, 88, 88, 88 ] ],
	[[ 94, 94, 85, 89 ],
     [ 94, 94, 93, 93 ],
	[ 90, 91, 92, 90 ],
	[ 95, 95, 95, 95 ],
	[ 88, 88, 88, 88 ]],
	[ [ 78, 80, 80, 85 ],
    [ 98, 98, 98, 95 ],
	[ 88, 87, 85, 80 ],
	[ 81, 85, 83, 86 ],
	[ 88, 88, 88, 88 ] ] ]
    
])
    v=self.comboBox_7.currentText()
    if v == '1':
       i=0
    if v == '5':
       i=1
    if v == '10':
       i=2
    if v == '20':
       i=3
    d=self.comboBox_8.currentText()
    if d == '30':
       j=0
    if d == '60':
       j=1
    if d == '90':
       j=2
    c=self.comboBox_9.currentText()
    if c == "road":
       k=0
    if c == "grass":
       k=1
    if c == "forest":
       k=2
    if c == "desert":
       k=3
    if c == "snow":
       k=4
    t=self.comboBox_10.currentText()
    if t == '8':
       l=0
    if t == '12':
       l=1
    if t == '16':
       l=2
    if t == '20':
       l=3
    result = Confidence[l][j][k][i]
    return result


def calculate_b(self):
    global i,j,k,l
    Confidence=numpy.array([                  
	[ [ [ 48, 56, 64, 79],
    [ 55, 59, 63, 75 ],
	[ 56, 66, 70, 72 ],
	[ 60, 65, 68, 69 ],
	[ 67, 67, 67, 67 ] ],
	[[ 50, 58, 62, 64 ],
     [ 59, 64, 65, 66 ],
	[ 47, 54, 60, 67 ],
	[ 55, 65, 70, 78 ],
	[ 67, 67, 67, 67 ] ],
	[ [ 76, 86, 90, 93 ],
    [ 70, 73, 80, 85 ],
	[ 54, 65, 66, 70 ],
	[ 40, 54, 59, 67 ],
	[ 67, 67, 67, 67 ]  ] ],
	[ 
	[ [ 61, 71, 73, 81 ],
    [ 49, 55, 54, 51 ],
	[ 56, 68, 72, 73 ],
	[ 70, 71, 69, 68 ],
	[ 67, 67, 67, 67 ]  ],
	[ [ 60, 65, 68, 66 ],
    [ 59, 65, 66, 70 ],
	[ 50, 65, 68, 70 ],
	[ 70, 71, 80, 84 ],
	[ 67, 67, 67, 67 ]  ],
	[[ 78, 83, 85, 86 ],
     [ 70, 78, 83, 85 ],
	[ 42, 43, 42, 43 ],
	[ 52, 60, 63, 69 ],
	[ 67, 67, 67, 67 ]  ] ],
	[ 
	[ [ 51, 70, 75, 86 ],
    [ 59, 62, 63, 65 ],
	[ 51, 68, 73, 80 ],
	[ 71, 75, 76, 78 ],
	[ 67, 67, 67, 67 ]  ],
	[ [ 64, 64, 68, 69 ],
    [ 59, 69, 71, 75 ],
	[ 48, 63, 67, 71 ],
	[ 67, 78, 82, 89 ],
	[ 67, 67, 67, 67 ] ],
	[ [ 80, 89, 90, 91 ],
    [ 83, 91, 94, 96 ],
	[ 62, 75, 78, 77 ],
	[ 52, 63, 67, 73 ],
	[ 67, 67, 67, 67 ]  ] ],
    [ 
	[[ 61, 73, 78, 86],
     [ 70, 68, 71, 76 ],
	[ 68, 77, 75, 73 ],
	[ 70, 73, 75, 74 ],
	[ 67, 67, 67, 67 ]  ],
	[[ 61, 66, 68, 68 ],
     [ 63, 65, 67, 66 ],
	[ 57, 62, 65, 70 ],
	[ 65, 72, 79, 87 ],
	[ 67, 67, 67, 67 ] ],
	[ [ 59, 65, 70, 78 ],
    [ 80, 87, 89, 89 ],
	[ 67, 70, 79, 72 ],
	[ 51, 60, 62, 66 ],
	[ 67, 67, 67, 67 ]  ] ]
    
])
    v=self.comboBox_7.currentText()
    if v == '1':
       i=0
    if v == '5':
       i=1
    if v == '10':
       i=2
    if v == '20':
       i=3
    d=self.comboBox_8.currentText()
    if d == '30':
       j=0
    if d == '60':
       j=1
    if d == '90':
       j=2
    c=self.comboBox_9.currentText()
    if c == "road":
       k=0
    if c == "grass":
       k=1
    if c == "forest":
       k=2
    if c == "desert":
       k=3
    if c == "snow":
       k=4
    t=self.comboBox_10.currentText()
    if t == '8':
       l=0
    if t == '12':
       l=1
    if t == '16':
       l=2
    if t == '20':
       l=3
    result = Confidence[l][j][k][i]
    return result

def imageShow(self): 
    v=self.comboBox_7.currentText()
    d=self.comboBox_8.currentText()
    c=self.comboBox_9.currentText()
    t=self.comboBox_10.currentText()
    s='v'+v +'_d'+d+'_'+c+'_'+t
    if c == "snow":
        h=numpy.random.randint (1,5)
        imagepath=path+'/picture/'+str(h)+'.png'
    if c != "snow":
        imagepath=path+'/picture/'+s+'.png'
    self.pic_label1.setPixmap(QtGui.QPixmap(imagepath).scaled(self.pic_label1.width(), self.pic_label1.height()))
    self.label_2.setText(imagepath)
    self.label.setText("正在进行示例图输出")

def detectImage(self):
   if self.pic_label1.pixmap() == None :
      msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有本地图片上传')
      msg_box.exec_()  
   else:
       sourcepath=self.label_2.text()
       if self.radioButton.isChecked():
        weightspath = path + "/runs/train/yolov5/weights/best.pt"
       if self.radioButton_2.isChecked():
        weightspath =path+"/runs/train/ca_yolov5/weights/best.pt"
       imgpath = infer(weightspath,sourcepath)
       self.pic_label1.setPixmap(QtGui.QPixmap(imgpath).scaled(self.pic_label1.width(), self.pic_label1.height()))
       self.label.setText("正在进行车辆检测")
   
# 选择本地图片上传
def openImage(self):
    global imgNamepath  
    imgNamepath, imgType = QFileDialog.getOpenFileName(self, "选择图片",)
    img = QtGui.QPixmap(imgNamepath).scaled(self.pic_label1.width(), self.pic_label1.height())
    self.pic_label1.setPixmap(img)
    self.label_2.setText(imgNamepath)
    self.label.setText("正在上传本地图片")

class mywinodw(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(mywinodw,self).__init__(parent)
        self.setupUi(self)   
        sys.stdout = Stream(newText=self.onUpdateText)
        self.groupBox.setStyleSheet("QGroupBox { border: 1px solid gray;}")
        self.groupBox_2.setStyleSheet("QGroupBox { border: 1px solid black;}")
        self.pushButton.clicked.connect(self.confidence_b)
        self.pushButton_2.clicked.connect(self.pic_example)
        self.pushButton_3.clicked.connect(self.detectpic)
        self.pushButton_4.clicked.connect(self.localpic)
        self.pushButton_5.clicked.connect(self.binaryseg)
        self.pushButton_9.clicked.connect(self.laplacian)
        self.pushButton_7.clicked.connect(self.equalhist)
        self.pushButton_8.clicked.connect(self.GaussianBlur)
        self.pushButton_6.clicked.connect(self.zeroseg)
        self.textEdit_2.setFocusPolicy(QtCore.Qt.NoFocus) #textEdit禁止编辑                       
        self.dial.setRange(25,75)
        self.dial.setNotchesVisible(True) 
        self.dial.valueChanged.connect(self.resizepic) 

   # GUI启用控制台输出
    def onUpdateText(self, text):
        #self.textEdit.clear()
        cursor = self.textEdit_2.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_2.setTextCursor(cursor)
        self.textEdit_2.ensureCursorVisible()

    def confidence(self):
        idex=calculate(self)
        str = "{}".format(idex)
        self.textlabel.setText(str+'%')

    def confidence_b(self):
        idex=calculate_b(self)
        str = "{}".format(idex)
        self.textlabel.setText(str+'%')
    
    def pic_example(self):
        imageShow(self)
    
    def localpic(self):
        openImage(self)

    def detectpic(self):
        detectImage(self)

    def resizepic(self):
       if self.pic_label1.pixmap() == None:
          msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有检测到图片')
          msg_box.exec_()
       else:
          scale=self.dial.value()/50
          image=self.pic_label1.pixmap().toImage()
          newWidth = int(image.size().width() * scale)
          newHeight = int(image.size().height() * scale)
          size = QSize(newWidth , newHeight )
          pixImg = QPixmap.fromImage(image.scaled(size))
          self.pic_label1.setPixmap(pixImg)

    def binaryseg(self):
       if self.pic_label1.pixmap() == None:
          msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有检测到图片')
          msg_box.exec_()
       else:
          self.label.setText("正在进行图片处理")
          img=self.pic_label1.pixmap().toImage()
          r, b = cv2.threshold(QImage2CV(img), 127, 255, cv2.THRESH_BINARY)
          qpixmap = QtGui.QPixmap(CV2QImage(b))
          self.pic_label1.setPixmap(qpixmap)

    def zeroseg(self):
       if self.pic_label1.pixmap() == None:
          msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有检测到图片')
          msg_box.exec_()  
       else:
          self.label.setText("正在进行图片处理")
          img=self.pic_label1.pixmap().toImage()
          r, b = cv2.threshold(QImage2CV(img), 127, 255, cv2.THRESH_TOZERO)
          qpixmap = QtGui.QPixmap(CV2QImage(b))
          self.pic_label1.setPixmap(qpixmap)
       
    
    def laplacian(self):
       if self.pic_label1.pixmap() == None:
          msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有检测到图片')
          msg_box.exec_()  
       else:
           self.label.setText("正在进行图片处理")
           img=self.pic_label1.pixmap().toImage()
           laplacian = cv2.Laplacian(QImage2CV(img), cv2.CV_64F)
           laplacian = cv2.convertScaleAbs(laplacian)
           qpixmap = QtGui.QPixmap(CV2QImage(laplacian))
           self.pic_label1.setPixmap(qpixmap)
    
    def equalhist(self):
       if self.pic_label1.pixmap() == None:
          msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有检测到图片')
          msg_box.exec_()
       else:
          self.label.setText("正在进行图片处理")
          img = self.pic_label1.pixmap().toImage()
          img = QImage2CV(img)
          img= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          equ = cv2.equalizeHist(img)
          qpixmap = QtGui.QPixmap(CV2grayQImage(equ))
          self.pic_label1.setPixmap(qpixmap)

    def GaussianBlur(self):
       if self.pic_label1.pixmap() == None:
          msg_box = QMessageBox(QMessageBox.Critical, '错误', '没有检测到图片')
          msg_box.exec_()
       else:
          self.label.setText("正在进行图片处理")
          img = self.pic_label1.pixmap().toImage()
          image = cv2.GaussianBlur(QImage2CV(img), (5, 5), 0)
          qpixmap = QtGui.QPixmap(CV2QImage(image))
          self.pic_label1.setPixmap(qpixmap)



class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()
      


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywinodw()
    # window= CandyWindow.createWindow(window, 'blueGreen')
    window.setObjectName("MainWindow")
    window.setStyleSheet("#MainWindow{border-image:url(C:/Users/Administrator/Desktop/qt5/picture/th2)}")
    window.show()
    sys.exit(app.exec_())