# HW2 Image Histogram

## 程式功能
本程式共有五組按鈕(Button)，分別為Select Image, Rotation, Histogram, Save, Exit。
1. Select Image: 選取圖片。
2. Rotation:每按下一次旋轉按鈕，旋轉90度。按兩次，則旋轉180度，以此類推。
3. Save Rotated Image: 儲存旋轉後的圖片。（注意：填入存檔檔名時，無需自行填入檔案格式，程式會自動帶入）
4. Histogram: 顯示圖片的直方圖。
5. Exit: 結束程式。

## 程式流程
![](/Images/hw2.jpg)


## 測試結果
範例一：紅、黃、綠三種顏色組成的圖片，從histogram來看，只出現三條線，因此可以得知此影像只有三種顏色。
![](/Images/hw2_1.jpg)
範例二則是有各種鮮豔的顏色，從histogram來看，長條圖型的分布皆位於中間區域，相較於前面兩張比較難得到圖片的特性，只能猜測圖片可能有許多顏色。
![](/Images/hw2_2.jpg)
範例三：如果這次先從histogram來看，長條圖分布皆位於左邊區域，有此可推出圖片色彩比較昏暗。
![](/Images/hw2_3.jpg)

## 心得
這次比較大的挑戰有三點。第一，如何將圖形介面分成兩個部分，一部分為PyQt、另一個部分為Matplotlib，花了一段時間查詢如何組合兩種library。第二，histogram的正規化以及colorbar的顯示也做了許多處理。第三，將檔案打包成exe檔，由於作業一沒有呼叫到太多的library，但這次不但使用了openCV，也使用了matplotlib等等library，因此在打包的過程中遇到了許多錯誤，還好在多方嘗試後，得以成功打包。