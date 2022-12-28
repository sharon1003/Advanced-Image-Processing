# tt.py

import cv2

path = "./dataset/traindata/ok/ok_29.jpg"
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
# _, output = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
_, output = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
output = cv2.resize(output, (512, 512))
cv2.imshow('My Image', output)

# 按下任意鍵則關閉所有視窗
cv2.waitKey(0)
cv2.destroyAllWindows()