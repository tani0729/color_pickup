#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import Pillow
from Pillow import Image, ImageDraw
import cv2
import sklearn
from sklearn.cluster import KMeans
import os
import numpy as np
def get_main_color(img_path):
    cv2_img = cv2.imread(img_path)#画像読み込み
    height = cv2_img.shape[0]
    width = cv2_img.shape[1]
    cv2_img = cv2.resize(cv2_img , (int(width*0.3), int(height*0.3)))
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)#BGRとRGBを変換
    cv2_img = cv2_img.reshape(
        (cv2_img.shape[0] * cv2_img.shape[1], 3))#データ量を3から２へ
    cluster = KMeans(n_clusters=5)#クラスター数を指定する
    cluster.fit(X=cv2_img)#クラスタリングを行い、cluster_centers_にRGB値を格納
    cluster_centers_arr = cluster.cluster_centers_.astype(
        int, copy=False)#格納されたRGB値の小数を消す
    IMG_SIZE = 64#カラーパレットの一1色分の大きさ
    MARGIN = 15
    width = IMG_SIZE * 5 + MARGIN * 2
    height = IMG_SIZE + MARGIN * 2 # 幅と高さ64px × 横並び5画像 + 上下左右余白15pxずつの画像を作成

    tiled_color_img = Image.new(
        mode='RGB', size=(width, height), color='#333333')#作成した画像をグレーにする

    for i, rgb_arr in enumerate(cluster_centers_arr):#iにインデックスの数字(5)、rgb_arrに上で取得したリストの要素(RGB値)
        color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)#RGB値をHEXに変換してPILに渡す
        color_hex_rev = '#%02x%02x%02x' % tuple(255-rgb_arr)#反対色のRGB値をHEXに変換してPILに渡す
        color_img = Image.new(
            mode='RGB', size=(IMG_SIZE, IMG_SIZE),#求めた色の正方形の画像を出力
            color=color_hex_str)
        draw = ImageDraw.Draw(color_img)#作成した画像の上にImageDrawインスタンスを作る
        draw.text((0,0),color_hex_str)#画像にHEXをいれる
        draw.text((21,54),color_hex_rev,color_hex_rev,)
        tiled_color_img.paste(
            im=color_img,
            box=(MARGIN + IMG_SIZE * i, MARGIN))#グレーの画像に各クラスタの色の画像をペーストしていく

    new_image = np.array(tiled_color_img, dtype=np.uint8)#PillowからCV2に変更
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)

    path ='/Users/tani/Pictures'#保存先指定
    cv2.imshow('image',new_image)#imageというウィンドウで表示
    k = cv2.waitKey(0)#何かボタンを押すまで待つ
    if k == ord('e'):  #Eを押した場合
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(0)#保存せずに取り消し
    elif k == ord('s'):#Sを押した場合
       #名前用に乱数生成 i =str(img_path)
        i =str(random.randint(1,100))#名前用に乱数生成
        cv2.imwrite(os.path.join(path,'colorpalette'+i+'.jpg'),new_image)#保存
        cv2.waitKey(0)
        cv2.destroyAllWindows()#表示取り消し
        cv2.waitKey(0)



