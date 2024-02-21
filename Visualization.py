import cv2
import numpy as np
import json
import sys
import random
import os
import shutil
import dbconfig
import datetime
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from ImgProcessLib import foldImgResize


def date_parser():
    tonow = datetime.datetime.now()
    year = tonow.year
    mon = tonow.month
    day = tonow.day
    hour = tonow.hour
    minute = tonow.minute
    second = tonow.second
    microsecond = tonow.microsecond
    return str(year)+'_'+str(mon)+'_'+str(day)+'_'+str(hour)+'_'+str(minute)+'_'+str(second)+'_'+str(microsecond)
    #return str(microsecond)

def prepareImgs(imagePath,reshape):
    '''
    資料夾下的前置準備
    @input
    `imagePath:`影像所在資料夾路徑
    `reshape:`是否要拉成一維array，PCA需要輸入一維array
    @output
    `imgList:`回傳所有影像List
    '''
    imageFileName = os.listdir(f'{imagePath}')
    #圖片大小
    img =  cv2.imread(f'{imagePath}/{imageFileName[0]}')
    w,h,_ = img.shape
    #縮放比例(減少分群時耗時)
    ratio = 2
    #呼叫自建Lib處理每張影像大小回傳List
    imgList = foldImgResize(imagePath, (w//ratio ,h//ratio),reshape)

    return imgList

def k_means(imgArr,cluster,method,savePath):
    '''
    經過降維方法後 使用k-means對影像進行分群
    @input
    `imagePath:`影像所在資料夾路徑，先做影像處理的準備
    `cluster:`要分的群數量
    `method:`使用的降維方法
    `savePath:`結果儲存路徑
    '''
    
    kmeans = KMeans(n_clusters=cluster).fit(imgArr)
    centroids =kmeans.cluster_centers_
    labels= kmeans.labels_
    imgArr = np.array(imgArr)
    #print(imgArr.shape[1])
    
    #檔案儲存名稱
    save_name =  date_parser() +'_'+method+'.jpg'

    #根據維度繪圖
    dm = imgArr.shape[1]
    if dm == 2:
        #print(imgArr)
        plt.figure()
        for i in range(0,cluster):
            plt.scatter(imgArr[labels==i,0],imgArr[labels==i,1], label=i)
        plt.plot(centroids[:,0],centroids[:,1],'o',markersize=5,marker='x', label='centroids')
        plt.legend(loc='best')
        plt.savefig(f'{savePath}/{save_name}')
        #plt.show()
        

    elif dm == 3:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in range(0,cluster):
            ax.scatter(imgArr[labels==i,0],imgArr[labels==i,1],imgArr[labels==i,2], label=i)

        ax.plot(centroids[:,0],centroids[:,1],centroids[:,2],'o',markersize=5,marker='x', label='centroids')
        ax.legend(loc='best')
        plt.savefig(f'{savePath}/{save_name}')
        #plt.show()
        

    return save_name
    
def t_SNE(imagePath,components,reshape=False):
    '''
    使用t_SNE進行降維
    @input
    `imagePath:`影像所在資料夾路徑，先做影像處理的準備
    `components:`要下降到多少維度
    `reshape:`是否要拉成一維
    @output
    `imgArr:`降維完的list
    '''
    imgList = prepareImgs(imagePath,reshape)
    #print(len(imgList))
    imgList = np.array(imgList)
    #print(imgList.shape)
    imgArr = TSNE(n_components=components,init='random',perplexity=imgList.shape[0]//5).fit_transform(imgList)
    imgArr = np.array(imgArr)
    #print(imgArr.shape)
    return imgArr

def PCA_(imagePath,components,reshape=False):
    '''
    使用PCA進行降維
    @input
    `imagePath:`影像所在資料夾路徑，先做影像處理的準備
    `components:`要下降到多少維度
    `reshape:`是否要拉成一維
    @output
    `imgArr:`降維完的list
    '''
    imgList = prepareImgs(imagePath,reshape)
    #print(len(imgList))
    imgArr = PCA(n_components=components).fit_transform(imgList)
    imgArr = np.array(imgArr)
    return imgArr

currentPath = os.path.dirname(__file__)
imagePath = f'{currentPath}/visual'
resultSavePath = f'{currentPath}/visual_result/'


user_id = sys.argv[1]
method = sys.argv[2]
draw_method = sys.argv[3]
kmeans = sys.argv[4]
#print(sys.argv)

'''
user_id = 1
method = 't_SNE'
draw_method = 3
kmeans = 4
'''


visual_arr = [method,draw_method,kmeans]

result = {
          'User_id': user_id,
          'Method': method,
          'Draw_method': draw_method,
          'K_means': kmeans,
          }


#連接資料庫
cursor = dbconfig.conn.cursor()
records = []


saveParm={}

#判斷使用方法
if method == "PCA":
    imgArr = PCA_(imagePath,int(draw_method),reshape=True)
    save_name = k_means(imgArr,int(kmeans),method='PCA'
                    ,savePath=resultSavePath)
    records.append((user_id,save_name))
    saveParm = {'User_id':user_id,
                'save_name':save_name}

elif method == "t_SNE":
    imgArr = t_SNE(imagePath,int(draw_method),reshape=True)
    save_name = k_means(imgArr,int(kmeans),method='tSNE'
                    ,savePath=resultSavePath)
    records.append((user_id,save_name))
    saveParm = {'User_id':user_id,
                'save_name':save_name}

#寫入資料庫
inserDb = 'INSERT INTO Image_visual_result(owner,image_visual_result) VALUES (%s,%s);'
cursor = dbconfig.conn.cursor()
cursor.executemany(inserDb,records)
dbconfig.conn.commit()


try:
    shutil.rmtree(imagePath)
except:
    pass
os.makedirs(imagePath)




json = json.dumps(saveParm)
print(str(json))
sys.stdout.flush()