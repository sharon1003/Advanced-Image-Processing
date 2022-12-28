# pra.py
import cv2

path = "./dataset/traindata/ok/ok_1.jpg"

img = cv2.imread(path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
# # output1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# img_gray = cv2.medianBlur(img_gray, 9)   # 模糊化
# output1 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
# output1 = cv2.resize(output1, (256, 256))

# img_gray2 = cv2.medianBlur(img_gray, 5)   # 模糊化
# output2 = cv2.adaptiveThreshold(img_gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# ret, output2 = cv2.threshold(img_gray2, 145, 255, cv2.THRESH_BINARY_INV)     # 如果大於 127 就等於 255，反之等於 0。
_, output1 = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY_INV) # Threshold Binary：即二值化，將大於閾值的灰度值設為最大灰度值，小於閾值的值設為0。
output1 = cv2.resize(output1, (256, 256))


cv2.imshow('oxxostudio1', output1)
# cv2.imshow('oxxostudio2', output2)
cv2.waitKey(0)
cv2.destroyAllWindows()