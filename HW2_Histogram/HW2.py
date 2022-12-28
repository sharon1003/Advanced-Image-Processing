# hw2.py

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import copy
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from setuptools._distutils import log, dir_util, file_util, archive_util




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



class MyWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle('AIP_61147006S')
		self.photo_Ori = PhotoLabel_Origin()
		self.photo_trans = PhotoLabel_Transform()
		# (x, y, width, height)
		self.setGeometry(150, 200, 1300, 500)

		self.figure = plt.figure(figsize=(30,30)) # 設定影像大小
		self.canvas = FigureCanvas(self.figure)

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
		

		# Save Image
		self.save_btn = QPushButton('Save Rotated Image', self)
		self.layout.addWidget(self.save_btn, 0, 2, Qt.AlignHCenter)
		self.save_btn.setEnabled(False)
		self.save_btn.clicked.connect(self.save_image)
		

		# Histogram
		self.histogram_btn = QPushButton('Histogram', self)
		self.layout.addWidget(self.histogram_btn, 0, 3, Qt.AlignHCenter)
		self.histogram_btn.setEnabled(False)
		self.histogram_btn.clicked.connect(self.Histogram)

		# Quit Button
		self.quit_btn = QPushButton("Exit", self)
		self.layout.addWidget(self.quit_btn, 0, 4, Qt.AlignHCenter)
		self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

		self.layout.addWidget(self.photo_Ori, 1, 0, 4, 2)
		self.layout.addWidget(self.canvas, 1, 2, 4, 3)
		# self.layout.addWidget(self.photo_trans, 1, 3, 4, 2)	
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
		self.image = cv2.imread(filename, cv2.IMREAD_COLOR)
		# opencv的接口使用BGR，而matplotlib.pyplot則是RGB模式
		b, g, r = cv2.split(self.image)
		# print(r)
		self.image = cv2.merge([r, g, b])
		# 顯示在右手邊
		temp = QPixmap(filename).toImage()
		result = temp.scaled(480, 360, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
		self.photo_Ori.setPixmap(QPixmap(result))
		self.histogram_btn.setEnabled(True)

	# Rotate Image
	def rotate_image(self):
		self.figure.clear()
		self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
		draw = self.figure.add_subplot(111)
		draw.imshow(self.image)
		draw.set_xlabel('Width')
		draw.set_ylabel('Height')
		draw.set_title('Rotated Image')
		self.canvas.draw()
		self.save_btn.setEnabled(True)

	# Save Image
	def save_image(self):
		filename, _ = QFileDialog.getSaveFileName(self, 'Save Image', QDir.currentPath())
		if filename:
			filename = filename+"."+self.fileformat
			print(filename)
			cv2.imwrite(filename, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

	def Histogram(self):

		# 再轉成灰階圖片
		print("press histogram")
		self.figure.clear()
		draw = self.figure.add_subplot(10, 1, (1, 9))
		inten_bar = self.figure.add_subplot(10, 1, 10)
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

		hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
		hist = np.reshape(hist, (1, 256))

		# 正規化hist[0]
		norm = normalize(hist[0], hist[0].min(), hist[0].max())
		
		draw.bar(range(1, 257), norm)
		draw.plot(hist)
		draw.get_xaxis().set_visible(False)

		# draw.set_ylim(0, np.mean(hist[0])) # limited the y-axes
		draw.set_ylabel('Number of Pixel (Normalized)')
		draw.set_title('Histogram')

		# draw the legend of colorbar
		cmap1 = copy.copy(cm.Greys)
		cmap1 = cmap1.reversed()
		norm1 = mcolors.Normalize(vmin=0, vmax=300)
		im1 = cm.ScalarMappable(norm=norm1, cmap=cmap1)
		cbar1 = self.figure.colorbar(
			im1, cax=inten_bar, orientation='horizontal',
			ticks=np.linspace(0, 250, 6),
			label='Intensity'
		)

		self.canvas.draw()

# 正規化
def normalize(arr, t_min, t_max):
	for i, val in enumerate(arr):
		arr[i] = (val - t_min) / (t_max - t_min)
	return arr

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
