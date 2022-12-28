import cv2

CLIP_X1, CLIP_Y1, CLIP_X2, CLIP_Y2 = 160, 140, 400, 360

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    # 套用自適應二值化黑白影像
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
    frame = cv2.flip(frame, 1) # 圖像水平翻轉
    cv2.rectangle(frame, (CLIP_X1, CLIP_Y1), (CLIP_X2, CLIP_Y2), (0,255,0) ,1) # 框出ROI位置

    ROI = frame[CLIP_Y1:CLIP_Y2, CLIP_X1:CLIP_X2] # ROI的大小
    ROI1 = cv2.resize(ROI, (128, 128))  # ROI resize
    ROI = cv2.cvtColor(ROI1, cv2.COLOR_BGR2GRAY) # ROI 轉灰階
    _, ROI = cv2.threshold(ROI, 100, 255, cv2.THRESH_BINARY)
    SHOWROI = cv2.resize(ROI, (256, 256)) # ROI resize
    # _, output2 = cv2.threshold(SHOWROI, wzs, 255, image_q) # Black Background is better for prediction
    cv2.imshow("ROI", SHOWROI)
    # ret, output = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)     # 如果大於 127 就等於 255，反之等於 0。
    # ret, output = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV) # 如果大於 127 就等於 0，反之等於 255。
    # ret, output = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TRUNC)      # 如果大於 127 就等於 127，反之數值不變。
    # ret, output = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TOZERO)     # 如果大於 127 數值不變，反之數值等於 0。
    # ret, output = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TOZERO_INV) # 如果大於 127 等於 0，反之數值不變。

    # img_gray = cv2.medianBlur(img_gray, 5)
    # output = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow('studio', frame)
    if cv2.waitKey(1) == ord('q'):
        break       # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()