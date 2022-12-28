# HW4 Convolution: Image Smoothing and edge detection

## 程式功能
本程式共有五組按鈕(Button)，分別為Select Image, Rotation, Convolution Filter, Default Filter, Exit。
1. Select Image: 選取圖片。
2. Rotation:每按下一次旋轉按鈕，旋轉90度。按兩次，則旋轉180度，以此類推。
3. Convolution Filter: 使用者可以自行輸入喜歡的Filter Masks。
4. Default Filter: 預設四個Convolution Filter，分別是邊緣偵測、水平偵測、垂直偵測和平滑化。
5. Exit: 結束程式。

## 程式流程
![](/Images/hw4.jpg)


## 測試結果
範例一: 為邊緣偵測(Edge Detection)之測試結果。右圖為經過5\*5 Filter Mask之結果。由下圖可觀察，圖中只將Lego外圍的字樣給印出。
範
![](/Images/hw4_1.jpg)
範例二: 為水平偵測之測試結果。右圖為經過5\*5 Filter Mask之結果。由下圖可觀察，相較於其他線條，水平線條更為明顯。
![](/Images/hw4_1.jpg)

## 心得
這次的convolution filter實作，非常有趣，使用自己手刻的convolution2D，套用到不同的filter mask，感覺就像是在做一個Photoshop。本次遇到的問題為np.array中的型態，會影響到imshow輸出。如果型態不符合的話，有可能會輸出程一張全白的影像。另外，就是由使用者自行輸入filter mask，這邊還需要額外做一些文字的處理，從先前的文字轉為數字，並轉換成kernel的格式，並放入convolution2D函式中。