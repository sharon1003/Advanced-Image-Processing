# HW5 Histogram Equalization

## 程式功能
本程式共有五組按鈕(Button)，分別為Select Image, Rotation, Convolution Filter, Default Filter, Exit。
1. Select Image: 選取圖片。
2. Rotation:每按下一次旋轉按鈕，旋轉90度。按兩次，則旋轉180度，以此類推。
3. Histogram display: 顯示出原圖與均質化後的直方圖。
4. Histogram equalization: 灰階直方圖均化。
5. Exit: 結束程式。

## 程式流程
![](/Images/hw5.jpg)


## 測試結果
範例一為手勢圖像灰階均質化之測試結果，手部很明顯可以看到原本較白的部分，因為均質化的效果，顏色變得較灰一些。
![](/Images/hw5_1.jpg)
範例二為灰階均質化之測試結果，原本愛因斯坦的圖片整體顏色較暗淡，經過均質化後，整體亮了許多。
![](/Images/hw5_2.jpg)

## 心得
這次的演算法相較上次簡單許多，也可以看到明顯的效果。尤其是在愛因斯坦圖片的那張，更能感受到灰皆均質化的威力。灰階均質化的應用主要可以將原本不明顯的顏色區域，加強其對比效果。在醫學影像上，可以照射出一些細小血管的部分，在影像處理時，也可以讓原本顏色昏暗，變得明亮。