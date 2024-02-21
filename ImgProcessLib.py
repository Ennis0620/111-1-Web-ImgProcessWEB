import cv2
import numpy as np
import json,sys 
import random
import os
import datetime

def vertical_flip(img):
    '''
    垂直翻轉
    @input
    `img:`影像
    '''
    v_img = cv2.flip(img, 0)
    return v_img

def horizontal_flip(img):
    '''
    水平翻轉
    @input
    `img:`影像
    '''
    h_img = cv2.flip(img, 1)
    return h_img

def histogramEqualColor(img):
    '''
    彩色直方圖均化
    @input
    `img:`影像(須為RGB)
    '''
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    print(len(channels))
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    hEC_img = cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return hEC_img    

def adjust_gamma(img,gamma):
    '''
    gamma correction亮度調整
    @input
    `img:`影像
    `gamma:`小數越大代表越亮，gamma=1為原圖
    '''
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    gC_img = cv2.LUT(img, table)    
    return gC_img

def rotation(img,angle):
    '''
    rotation 左右旋轉
    @input
    `img:`影像
    `angle:`要旋轉的角度，旋轉角度(-順時針 / +逆時針)
    '''
    (h, w, d) = img.shape # 讀取圖片大小
    center = (w // 2, h // 2) # 找到圖片中心
    # 第一個參數旋轉中心，第二個參數旋轉角度(-順時針/+逆時針)，第三個參數縮放比例
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 第三個參數變化後的圖片大小
    rotate_img = cv2.warpAffine(img, M, (w, h))
    return rotate_img


def erode(img,kernel_size,iterations):
    '''
    形態學:侵蝕
    @input
    `img:`影像
    `kernel_size:`kernel 捲積大小為 3x3，可以改成 5x5 或 7x7 較為常見
    `iterations:`需要做幾次
    '''
    kernel = np.ones((kernel_size,kernel_size), np.uint8)

    try:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    except:
        pass

    img = cv2.erode(img,kernel,iterations = iterations)
    return img

def dilate(img,kernel_size,iterations):
    '''
    形態學:膨脹
    @input
    `img:`影像
    `kernel_size:`kernel 捲積大小為 3x3，可以改成 5x5 或 7x7 較為常見
    `iterations:`需要做幾次
    '''
    kernel = np.ones((kernel_size,kernel_size), np.uint8)

    try:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    except:
        pass

    img = cv2.dilate(img,kernel,iterations = iterations)
    return img

def opening(img,kernel_size):
    '''
    形態學:開運算(先erode後dilate)
    @input
    `img:`影像
    `kernel_size:`kernel 捲積大小為 3x3，可以改成 5x5 或 7x7 較為常見
    '''
    kernel = np.ones((kernel_size,kernel_size), np.uint8)

    try:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    except:
        pass
    
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img

def closing(img,kernel_size):
    '''
    形態學:閉運算(先dilate後erode)
    @input
    `img:`影像
    `kernel_size:`kernel 捲積大小為 3x3，可以改成 5x5 或 7x7 較為常見
    '''
    kernel = np.ones((kernel_size,kernel_size), np.uint8)

    try:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    except:
        pass

    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img

def gradient(img,kernel_size):
    '''
    形態學:Gradient運算
    @input
    `img:`影像
    `kernel_size:`kernel 捲積大小為 3x3，可以改成 5x5 或 7x7 較為常見
    '''
    kernel = np.ones((kernel_size,kernel_size), np.uint8)

    try:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    except:
        pass

    img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    return img

def split_channel():
    '''
    將RGB影像分成3種Channel
    @input
    `img:`彩色影像
    @output
    `imgList:`3個channel(R、G、B)分別的影像List
    '''
    



def foldImgResize(imgPath,size,reshape=False):
    '''
    資料夾影像resize大小
    @input
    `imgPath:`影像
    `resize:`要縮放的影像大小(w,h)
    `reshape:`是否要拉成一維array
    @output
    `imageList:`reisze後的影像list
    '''
    imageList = []
    imageFileName = os.listdir(f'{imgPath}')
    for imgName in imageFileName:
        img = cv2.imread(f'{imgPath}/{imgName}')
        img = cv2.resize(img,size)/255.0
        if reshape:
            img = np.reshape(img,-1)
            imageList.append(img)
        else:
            imageList.append(img)
    
    return imageList


if __name__=="__main__":
    img = cv2.imread("./test.jpg")
    #img = adjust_gamma(img,gamma=1.0)
    #img =  rotation(img,10)
    img = histogramEqualColor(img)
    #img = gradient(img,3)
    #img = opening(img,3)
    #img = adjust_gamma(img,gamma=1.3)

    cv2.imshow('m',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
