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
		self.GetIntlineEdit.setTextGeometry(QRect(150, 30, 150, 31))
		self.GetIntlineEdit.setText("請輸入convolution masks")
		

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
		# self.photo_trans = PhotoLabel_Transform()
		# (x, y, width, height)
		self.setGeometry(100, 100, 1200, 800)

		# self.figure0 = plt.figure(figsize=(600,400)) # 設定影像大小
		# self.canvas0 = FigureCanvas(self.figure0)

		self.figure1 = plt.figure(figsize=(600,400)) # 設定影像大小
		self.canvas1 = FigureCanvas(self.figure1)

		# self.figure2 = plt.figure(figsize=(500,500)) # 設定影像大小
		# self.canvas2 = FigureCanvas(self.figure2)

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
		
		# # Histogram_Salt and Pepper
		# self.hist_salt_btn = QPushButton('Histogram of Salt and Pepper noise', self)
		# self.layout.addWidget(self.hist_salt_btn, 0, 5, Qt.AlignHCenter)
		# self.hist_salt_btn.setEnabled(False)
		# self.hist_salt_btn.clicked.connect(self.Histogram_Salt_pepper)
		

		# # Histogram Guassian
		# self.hist_Gau_btn = QPushButton('Histogram of Gaussian noise', self)
		# self.layout.addWidget(self.hist_Gau_btn, 0, 3, Qt.AlignHCenter)
		# self.hist_Gau_btn.setEnabled(False)
		# self.hist_Gau_btn.clicked.connect(self.Histogram_Gau)

		# Quit Button
		self.quit_btn = QPushButton("Exit", self)
		self.layout.addWidget(self.quit_btn, 0, 4, Qt.AlignHCenter)
		self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

		# Convolution
		self.convolution_btn = QPushButton("Convolution filter", self)
		self.layout.addWidget(self.convolution_btn, 0, 2, Qt.AlignHCenter)
		self.convolution_btn.setEnabled(False)
		self.convolution_btn.clicked.connect(self.convolution2D)

		# test
		self.item_btn = QPushButton("Default Kernel", self)
		self.layout.addWidget(self.item_btn, 0, 3, Qt.AlignHCenter)
		self.item_btn.setEnabled(False)
		self.item_btn.clicked.connect(self.item)

		# # Gaussian
		# self.Gaussian_btn = QPushButton("Gaussian", self)
		# self.layout.addWidget(self.Gaussian_btn, 0, 2, Qt.AlignHCenter)
		# self.Gaussian_btn.clicked.connect(self.GaussianGetInteger)

		# # Salt & Pepper
		# self.saltAndPepper_btn = QPushButton("Salt&Pepper", self)
		# self.layout.addWidget(self.saltAndPepper_btn, 0, 4, Qt.AlignHCenter)
		# self.saltAndPepper_btn.clicked.connect(self.SaltAndPepper)

		self.layout.addWidget(self.photo_Ori, 1, 0, 4, 2)
		self.layout.addWidget(self.canvas1, 1, 2, 4, 3)
		# self.layout.addWidget(self.canvas2, 4, 0, 3, 7)

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
		# print(filename)
		self.image = cv2.imread(filename)
		# opencv的接口使用BGR，而matplotlib.pyplot則是RGB模式
		# b, g, r = cv2.split(self.image)
		# self.image = cv2.merge([r, g, b])
		self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
		# 顯示在右手邊
		temp = QPixmap(filename).toImage()
		result = temp.scaled(480, 360, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
		grayscale = result.convertToFormat(QImage.Format_Grayscale8)
		pixmap = QPixmap.fromImage(grayscale)
		self.photo_Ori.setPixmap(pixmap)
		self.convolution_btn.setEnabled(True)
		self.item_btn.setEnabled(True)

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

	def convolution2D(self):
		while(1):
			text1, ok1 = QInputDialog.getText(self, 'Convolution filter', '請輸入convolution masks之分數部分\
\n 範例格式：分子/分母')
			
			if not ok1:
				break

			text2, ok2 = QInputDialog.getText(self, 'Convolution filter', '請輸入convolution masks: \
\n 範例格式：\n [[1, 1, 1, 1, 1],\n \
[1, 1, 1, 1, 1],\n \
[1, 1, 1, 1, 1],\n \
[1, 1, 1, 1, 1],\n \
[1, 1, 1, 1, 1]]')
			print(len(text2.split(',')))
			if len(text2.split(',')) >= 24:
				print(text1)
				print(text2)
				kernel = text_split(text1, text2)
				print(kernel)
				break
			elif not ok2:
				break
			else:
				QMessageBox.warning(self, "Warning", "請輸入大於5*5之Filter Mask", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)

		self.figure1.clear()

		if ok1 and ok2:

			gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

			new_image = convolution2D(gray, kernel)

			draw = self.figure1.add_subplot(111)
			draw.xaxis.set_ticks([])
			draw.yaxis.set_ticks([])
			draw.imshow(new_image, cmap="gray")

			self.canvas1.draw()

	def item(self):

		items = ("Edge Detection", "Averaging", "level detection", "Vertical detection")
		item, ok = QInputDialog.getItem(self, "Filter masks", "Select Filter masks", items, 0, False)
			
		if not ok:
			return

		if ok:

			gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
			kernel = np.zeros((3,3)) 

			if item == 'Edge Detection':
				kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
			if item == 'Averaging':
				kernel = np.ones((5, 5)) / 25
			if item == 'level detection':
				kernel = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
			if item == 'Vertical detection':
				kernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])

			print(item)
			print(kernel)
			
			self.figure1.clear()

			new_image = convolution2D(gray, kernel)

			draw = self.figure1.add_subplot(111)
			draw.xaxis.set_ticks([])
			draw.yaxis.set_ticks([])
			draw.imshow(new_image, cmap="gray", vmin=0, vmax=255)

			self.canvas1.draw()


	def Histogram_Gau(self):

		# 再轉成灰階圖片
		print("press Histogram_Gau")

		self.figure2.clear()
		draw1 = self.figure2.add_subplot(1, 3, 1)
		draw2 = self.figure2.add_subplot(1, 3, 2)
		draw3 = self.figure2.add_subplot(1, 3, 3)


		gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

		hist_ori_img, bins = np.histogram(gray.ravel(), 256)
		draw1.bar(bins[:-1], hist_ori_img)
		draw1.get_yaxis().set_visible(False)
		# draw1.set_ylim(0, int(max(hist_ori_img)/2)) # limited the y-axes


		hist_filter, bins = np.histogram((self.Gau_filter).ravel(), 256)
		draw2.bar(bins[:-1], hist_filter)
		draw2.get_yaxis().set_visible(False)

		hist_aft_img, bins = np.histogram((self.Gau_img).ravel(), 256)
		draw3.bar(bins[:-1], hist_aft_img)
		draw3.get_yaxis().set_visible(False)
		# draw3.set_ylim(0, max(hist_ori_img)) # limited the y-axes


		self.canvas2.draw()

	def Histogram_Salt_pepper(self):

		# 再轉成灰階圖片
		print("press Histogram_Salt")

		self.figure2.clear()

		draw1 = self.figure2.add_subplot(1, 3, 1)
		draw2 = self.figure2.add_subplot(1, 3, 2)
		draw3 = self.figure2.add_subplot(1, 3, 3)

		gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
		
		hist_ori_img, bins = np.histogram(gray.ravel(), 256)
		draw1.bar(bins[:-1], hist_ori_img)
		draw1.get_yaxis().set_visible(False)
		# draw1.set_ylim(0, hist_ori_img)


		hist_filter, bins = np.histogram((self.salt_filter).ravel(), 256)
		draw2.bar(bins[:-1], hist_filter)
		draw2.get_yaxis().set_visible(False)

		hist_aft_img, bins = np.histogram((self.salt_img).ravel(), 256)
		draw3.bar(bins[:-1], hist_aft_img)
		draw3.get_yaxis().set_visible(False)
		# draw3.set_ylim(0, )

		self.canvas2.draw()

	def SaltAndPepper(self):
		print("get integer")
		# 預設值，最小值，最大值和步長
		percetage, okPressed = QInputDialog.getInt(self, "請輸入Salt and Pepper程度","Percentage:", 0, 0, 100, 1)
		if okPressed:
			print(percetage)

		row = np.shape(self.image)[0]
		col = np.shape(self.image)[1]	
		number_of_pixels = int(row * col * percetage * 0.01)
		print(row, col)
		new_img = np.zeros((row, col))

		gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
		row = np.shape(gray)[0]
		col = np.shape(gray)[1]


		for i in range(row):
			for j in range(col):
				new_img[i][j] = 255

		for i in range(int(number_of_pixels)):
			y = random.randint(0, row-1)
			x = random.randint(0, col-1)
			gray[y][x] = 255
			new_img[y][x] = 255

		for i in range(int(number_of_pixels)):
			y = random.randint(0, row-1)
			x = random.randint(0, col-1)
			gray[y][x] = 0
			new_img[y][x] = 0

		self.salt_filter = np.array(new_img)
		self.salt_img = gray

		self.figure1.clear()
		
		draw1 = self.figure1.add_subplot(1, 6, (1, 3))
		draw2 = self.figure1.add_subplot(1, 6, (4, 6))

		draw1.xaxis.set_ticks([])
		draw1.yaxis.set_ticks([])

		draw2.xaxis.set_ticks([])
		draw2.yaxis.set_ticks([])

		# 如果image只有一個channel的話，imshow是用colormap去印的，要特別指定才可以
		draw1.imshow(self.salt_filter, cmap="gray", vmin=0, vmax=255)
		draw2.imshow(self.salt_img, cmap="gray", vmin=0, vmax=255)

		self.hist_salt_btn.setEnabled(True)
		self.hist_Gau_btn.setEnabled(False)


		self.canvas1.draw()

	def GaussianGetInteger(self):
		print("get integer")
		mean, okPressed = QInputDialog.getInt(self, "請輸入標準差","Percentage:", 0, 0, 100, 1)
		if okPressed:
			print(mean)

		gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
		row = np.shape(gray)[0]
		col = np.shape(gray)[1]
		new_img = []

		# 隨機產生兩個值[0, 1]
		for i in range(0, row):
			tmp = []
			for j in range(0, col, 2):
				r = np.random.rand()
				q = np.random.rand()
				
				# 計算z1, z2
				z1 = mean * np.cos(2 * np.pi * q) * np.sqrt(-2 * np.log(r))
				z2 = mean * np.sin(2 * np.pi * q) * np.sqrt(-2 * np.log(r))

				t1 = gray[i][j] + z1
				t2 = gray[i][j+1] + z2

				if t1 < 0:		t1 = 0
				if t1 > 255:	t1 = 255
				if t2 < 0:		t2 = 0
				if t2 > 255:	t2 = 255

				gray[i][j] = int(t1)
				gray[i][j+1] = int(t2)
				tmp.append(z1)
				tmp.append(z2)

			new_img.append(tmp) # Gaussian所產生的圖片
		new_img = np.array(new_img)

		self.figure1.clear()
		self.Gau_filter = new_img
		self.Gau_img = gray
		
		draw1 = self.figure1.add_subplot(1, 6, (1, 3))
		draw2 = self.figure1.add_subplot(1, 6, (4, 6))

		draw1.xaxis.set_ticks([])
		draw1.yaxis.set_ticks([])

		draw2.xaxis.set_ticks([])
		draw2.yaxis.set_ticks([])
		# 如果image只有一個channel的話，imshow是用colormap去印的，要特別指定才可以
		draw1.imshow(self.Gau_filter, cmap="gray", vmin=0, vmax=255)
		draw2.imshow(self.Gau_img, cmap="gray", vmin=0, vmax=255)

		self.hist_Gau_btn.setEnabled(True)
		self.hist_salt_btn.setEnabled(False)


		self.canvas1.draw()

# 正規化
def normalize(arr):
	for i, val in enumerate(arr):
		arr[i] = np.log(int(arr[i]))
	return arr

def convolution2D(image, kernel, padding=2, strides=1):
	# 把kernel上下左右顛倒
	kernel = np.flipud(np.flipud(kernel))

	# 取得kernel大小
	kernel_x = kernel.shape[0]
	kernel_y = kernel.shape[1]

	image_x = image.shape[0]
	image_y = image.shape[1]

	# 利用公式取得padding與stride後convolution大小
	new_image_x = int(((image_x - kernel_x + 2 * padding) / strides) + 1)
	new_image_y = int(((image_y - kernel_y + 2 * padding) / strides) + 1)
	new_image = np.zeros((new_image_x, new_image_y))


	# 把padding放入
	if padding != 0:
		imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
		imagePadded[int(padding):int(-1*padding), int(padding):int(-1*padding)] = image
	else:
		imagePadded = image


	for y in range(image.shape[1]):
		# 如果stride超過影片大小
		if y > image.shape[1] - kernel_y: # kernel_y == 5
			break
		if y % strides == 0:
			for x in range(image.shape[0]):
				if x > image.shape[0] - kernel_x:
					break
				if x % strides == 0:
					# kernel 5*5 和 取影像x到x+5 y, y+5支5*5影像相乘
					tmp = (kernel * imagePadded[x:x+kernel_x, y:y+kernel_y]).sum()
					if tmp < 0:	tmp = 0
					if tmp > 255: tmp = 255
					new_image[x, y] = int(tmp)

	new_image = new_image.astype(np.uint8)   # 進行型別轉換，原本是np.float64

	return new_image

def text_split(fraction, matrix):

	index = fraction.index('/')

	s = ''
	for c in range(0, index):
		s += fraction[c]
	molecular = int(s)

	s = ''
	for c in range(index+1, len(fraction)):
		s += fraction[c]
	denominator = int(s)
	# denominator = int(fraction[index-1]) / int(fraction[index+1])

	arr = []
	tmp = []
	for c in matrix:
		if c == ']':
			arr.append(tmp)
			tmp = []
			continue
		if c.isdigit():
			tmp.append(int(c))

	arr.pop()

	print('molecular', molecular)
	print('denominator', denominator)
	
	arr = np.array(arr) / denominator
	return arr

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
