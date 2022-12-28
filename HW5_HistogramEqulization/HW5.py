# hw1.py

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import copy
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import random
from setuptools._distutils import log, dir_util, file_util, archive_util




class Ui_Form(object):
	def setupUi(self, Form):  
		self.GetIntlineEdit = QLineEdit(Form)
		self.GetIntlineEdit.setGeometry(QRect(150, 30, 150, 31))
		self.GetIntlineEdit.setText("")
		

class PhotoLabel_Origin(QLabel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setAlignment(Qt.AlignCenter)
		self.setText('\n\n Original Image \n\n')
		self.setStyleSheet('''
		QLabel {
			border: 4px dashed #aaa;
		}''')

	def setPixmap(self, *args, **kwargs):
		super().setPixmap(*args, **kwargs)
		self.setStyleSheet('''
		QLabel {
			border: None;
		}''')

class PhotoLabel_Transform(QLabel):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setAlignment(Qt.AlignCenter)
		self.setText('\n\n Rotated Image \n\n')
		self.setStyleSheet('''
		QLabel {
		    border: 4px dashed #aaa;
		}''')
    
	def setPixmap(self, *args, **kwargs):
		super().setPixmap(*args, **kwargs)
		self.setStyleSheet('''
		QLabel {
			border: None;
		}''')


class MyWidget(QWidget, Ui_Form):
	def __init__(self):
		super().__init__()
		self.initUI()
		self.flag = 0 # 用來判斷是否近入Gau_img
		# self.setupUi(self)

	def initUI(self):
		self.setWindowTitle('AIP_61147006S')
		self.photo_Ori = PhotoLabel_Origin()
		self.photo_trans = PhotoLabel_Transform()
		# (x, y, width, height)
		self.setGeometry(100, 100, 500, 1000)

		# 直方圖
		self.figure1 = plt.figure(figsize=(300,400)) # 設定影像大小
		self.canvas1 = FigureCanvas(self.figure1)

		# 雜訊
		self.figure2 = plt.figure(figsize=(300,400)) # 設定影像大小
		self.canvas2 = FigureCanvas(self.figure2)
		
		self.layout = QGridLayout()
		# Open file button
		self.select_btn = QPushButton('Select Image', self)
		self.layout.addWidget(self.select_btn, 0, 0, Qt.AlignHCenter)
		self.select_btn.clicked.connect(self.open_image)

		# Rotate file button
		self.rotate_btn = QPushButton('Rotation', self)
		self.layout.addWidget(self.rotate_btn, 0, 1, Qt.AlignHCenter)
		self.rotate_btn.setEnabled(False)
		self.rotate_btn.clicked.connect(self.rotate_image)

		# Histogram Guassian
		self.hist_dis_btn = QPushButton('Histogram Display', self)
		self.layout.addWidget(self.hist_dis_btn, 0, 2, Qt.AlignHCenter)
		self.hist_dis_btn.setEnabled(False)
		self.hist_dis_btn.clicked.connect(self.Histogram_display)

		# Salt & Pepper
		self.his_equ_btn = QPushButton("Histogram_equalization", self)
		self.layout.addWidget(self.his_equ_btn, 0, 3, Qt.AlignHCenter)
		self.his_equ_btn.setEnabled(False)
		self.his_equ_btn.clicked.connect(self.Histogram_equalization)

		# Quit Button
		self.quit_btn = QPushButton("Exit", self)
		self.layout.addWidget(self.quit_btn, 0, 4, Qt.AlignHCenter)
		self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

		self.layout.addWidget(self.photo_Ori, 1, 0, 2, 2)
		self.layout.addWidget(self.canvas1,   1, 2, 2, 5)
		self.layout.addWidget(self.canvas2,   3, 0, 2, 5)

		self.setLayout(self.layout)


	def open_image(self, filename=None):
		if not filename:
			self.rotate_btn.setEnabled(True)
			filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.bmp *.jpg *.ppm *.jpeg *.png)')
			if not filename:
				return

		# get file format
		self.filename = filename
		self.fileformat = (filename.split('/')[-1]).split('.')[-1]
		print(filename)
		self.image = cv2.imread(filename)
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
		temp = QPixmap(filename).toImage()
		result = temp.scaled(480, 360, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
		self.photo_Ori.setPixmap(QPixmap(result))
		self.his_equ_btn.setEnabled(True)



	# Rotate Image
	def rotate_image(self):
		self.figure1.clear()
		self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
		draw = self.figure1.add_subplot(111)
		draw.imshow(self.image)
		draw.set_xlabel('Width')
		draw.set_ylabel('Height')
		draw.set_title('Rotated Image')
		self.canvas1.draw()

	def Histogram_equalization(self):

		gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

		print("Previous gray\n", gray)
		N = np.shape(self.image)[0]
		M = np.shape(self.image)[1]

		H = np.zeros((256), dtype=int)
		# scan every pixel p in image
		for row in range(N):
			for col in range(M):
				H[gray[row][col]] += 1

		min_index = H[np.nonzero(H)][0]
		g_min = list(H).index(min_index)
		print("g_min", g_min)

		# Step 3. 
		Hc = np.zeros((256), dtype=int)
		Hc[0] = 0
		for index in range(1, 256):
			Hc[index] = Hc[index-1] + H[index]
		H_min = Hc[g_min]
		print("H_min", H_min)

		# Step 4.
		T = np.zeros((256), dtype=int)
		denominator = (M * N) - H_min 
		for index in range(256):
			numerator = Hc[index] - H_min
			T[index] = np.round((numerator / denominator) * 255)
		
		self.his_equ_gray = np.ones((N, M))
		# Step 5. rescan the image and write an output image with gray-levels gq
		for row in range(N):
			for col in range(M):
				self.his_equ_gray[row][col] = T[gray[row][col]]
		print("new gray\n", self.his_equ_gray)


		self.figure1.clear()
		draw1 = self.figure1.add_subplot(111)

		# 如果image只有一個channel的話，imshow是用colormap去印的，要特別指定才可以
		draw1.imshow(self.his_equ_gray, cmap="gray", vmin=0, vmax=255)
		
		self.hist_dis_btn.setEnabled(True)

		self.canvas1.draw()

	def Histogram_display(self):

		# 再轉成灰階圖片
		print("press Histogram_display")

		self.figure2.clear()
		draw1 = self.figure2.add_subplot(1, 2, 1)
		draw2 = self.figure2.add_subplot(1, 2, 2)

		gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

		hist_ori_img, bins = np.histogram(gray.ravel(), 256)
		draw1.bar(bins[:-1], hist_ori_img)
		draw1.get_yaxis().set_visible(False)

		hist_filter, bins = np.histogram((self.his_equ_gray).ravel(), 256)
		draw2.bar(bins[:-1], hist_filter)
		draw2.get_yaxis().set_visible(False)

		self.canvas2.draw()


# 正規化
def normalize(arr):
	for i, val in enumerate(arr):
		arr[i] = np.log(int(arr[i]))
	return arr

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
