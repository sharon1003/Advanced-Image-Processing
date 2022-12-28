# hw1.py

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


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
        self.setGeometry(200, 200, 1000, 150)

        layout = QGridLayout()
        self.setLayout(layout)

        # Open file button
        self.select_btn = QPushButton('Select Image', self)
        layout.addWidget(self.select_btn, 0, 0, Qt.AlignHCenter)
        self.select_btn.clicked.connect(self.open_image)

        # Rotate file button
        self.rotate_btn = QPushButton('Rotation', self)
        layout.addWidget(self.rotate_btn, 0, 1, Qt.AlignHCenter)
        self.rotate_btn.setEnabled(False)
        self.rotate_btn.clicked.connect(self.rotate_image)

        # Save Image
        self.save_btn = QPushButton('Save', self)
        layout.addWidget(self.save_btn, 0, 2, Qt.AlignHCenter)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_image)

        # Quit Button
        self.quit_btn = QPushButton("Exit", self)
        layout.addWidget(self.quit_btn, 0, 3, Qt.AlignHCenter)
        self.quit_btn.clicked.connect(QCoreApplication.instance().quit)

        layout.addWidget(self.photo_Ori, 1, 0)
        layout.addWidget(self.photo_trans, 1, 1)

    def open_image(self, filename=None):
        if not filename:
            self.rotate_btn.setEnabled(True)
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.bmp *.jpg *.ppm)')
            if not filename:
                return

        # get file format
        self.fileformat = (filename.split('/')[-1]).split('.')[-1]
        self.image = QPixmap(filename).toImage()
        result = self.image.scaled(480, 360, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.photo_Ori.setPixmap(QPixmap(result))

    # Rotate Image
    def rotate_image(self):
        transform = QTransform().rotate(90)
        self.image = self.image.transformed(transform)
        # 設定影像大小
        result = self.image.scaled(480, 360, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.photo_trans.setPixmap(QPixmap.fromImage(result))
        self.save_btn.setEnabled(True)

    # Save Image
    def save_image(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Image', QDir.currentPath())
        if filename:
            filename = filename+"."+self.fileformat
            print(filename)
            self.image.save(filename, (self.fileformat).upper(), -1) # -1 代表默認值


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
