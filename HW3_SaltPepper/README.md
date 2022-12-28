# HW3 Generation of Gaussian noise and salt-and-pepper noise

## 程式功能
本程式共有七組按鈕(Button)，分別為Select Image, Rotation, Gaussian, Histogram of Gaussian Noise, Salt Pepper, Histogram of Salt and Pepper noise, Exit。
1. Select Image: 選取圖片。
2. Rotation:每按下一次旋轉按鈕，旋轉90度。按兩次，則旋轉180度，以此類推。
3. Gaussian: 點下後，輸入標準差的比例，範圍為0-100，只接受整數輸入。
4. Histogram of Gaussian Noise: 顯示圖片的直方圖。
5. Salt Pepper: 點下後，輸入椒鹽雜訊的比例，範圍從0-100，只接受整數輸入。
6. Histogram of Salt and Pepper noise: 顯示出原圖、椒鹽雜訊圖與結合椒鹽雜訊的原圖之Histogram圖。
7. Exit: 結束程式。

## 程式流程
![](/Images/hw3.jpg)


## 測試結果
範例一：使用RGB三個顏色之圖片，並加入Gaussian Noise，輸入標準差：10。程式下方為測試結果圖。左下方原圖只呈現出三條線，但經過Gaussian Noise後，在右下方出現其他的直條圖，並呈現出高斯分布的形式。
![](/Images/hw3_1.jpg)
範例二：Gaussian Noise之測試結果，輸入標準差：50。程式下方為histogram測試結果圖。左下方原圖原本有很許多突出的直條線，經過Gaussian Noise後，在右下方結果呈現出平滑的曲線。
![](/Images/hw3_2.jpg)
範例三：Salt and Pepper Noise之測試結果。左下方為原圖檔之Histogram，椒鹽雜訊百分比輸入50後，同樣明顯地看到座下方的極值部分，銳減許多。另外，結合椒鹽雜訊後的圖片，也難以看出途中人物的表情。
![](/Images/hw3_3.jpg)
## 心得
這次所有的雜訊都使用手刻函式(Gaussian Noise, Salt and Pepper)，沒有使用到OpenCV內建的函式庫。比較困難的部分為當輸入的圖片大小不為偶數時，應該如何進行處理。解決辦法使用程式去判斷，當height或width為奇數時，將這些height-1或row-1，由於圖片Pixel數頗多，少掉一些Pixel值，也不至於影響對於整張圖的判斷。