import cv2
import numpy as np
import json
import sys
import random
import os
from ImgProcessLib import horizontal_flip, vertical_flip, histogramEqualColor, adjust_gamma, rotation
import dbconfig
import datetime


def date_parser():
    tonow = datetime.datetime.now()
    year = tonow.year
    mon = tonow.month
    day = tonow.day
    hour = tonow.hour
    minute = tonow.minute
    second = tonow.second
    microsecond = tonow.microsecond
    #return str(year)+'_'+str(mon)+'_'+str(day)+'_'+str(hour)+'_'+str(minute)+'_'+str(second)+'_'+str(microsecond)
    return str(microsecond)

def aug_func(img):
    if vf == 'on':
        #print('exec vf')
        img = vertical_flip(img)
    if hf == 'on':
        #print('exec hf')
        img = horizontal_flip(img)
    if hEC == "on":
        #print('exec hEC')
        img = histogramEqualColor(img)
    if a_gamma != "":
        #print('exec gmmma')
        img = adjust_gamma(img, float(a_gamma))
    if rt != "":
        img = rotation(img, float(rt))

    return img

currentPath = os.path.dirname(__file__)
#currentPath =  "H://NCNU//class//111-1_code//1_web//ImgProcessWEB"

img_path = f'{currentPath}/upload'
img_aug_path = f'{currentPath}/upload_aug'

'''
user_id = 1
vf = "on"
hf = "off"
hEC = "off"
a_gamma = "1.85"
aug_arr = [vf,hf,hEC,a_gamma]
'''

user_id = sys.argv[1]
vf = sys.argv[2]
hf = sys.argv[3]
hEC = sys.argv[4]
a_gamma = sys.argv[5]
rt = sys.argv[6]

aug_arr = [vf,hf,hEC,a_gamma,rt]


result = {'User_id': user_id,
          'Vertical_flip': vf,
          'Horizontal_flip': hf,
          'HistogramEqualColor': hEC,
          'Adjust_gamma': a_gamma,
          'Rotation': rt}

# 'Erode' : sys.argv[6],
# 'Dilate' : sys.argv[7],
# 'Opening' : sys.argv[8],
# 'Closing' : sys.argv[9],
# 'Gradient' : sys.argv[10],

#去DB找到所有影像路徑
cursor = dbconfig.conn.cursor()
cursor.execute(f'SELECT image_path from Image WHERE owner = {user_id}')

'''
img_name = cursor.fetchone()
img = cv2.imread(f'{img_path}/{img_name[0]}')
save_name = 'aug_' + date_parser() + '_' + img_name[0] 

if vf == 'on':
    print('exec vf')
    img = vertical_flip(img)
if hf == 'on':
    print('exec hf')
    img = horizontal_flip(img)
if hEC == "on":
    print('exec hEC')
    img = histogramEqualColor(img)
if a_gamma != "":
    print('exec gmmma')
    img = adjust_gamma(img, float(a_gamma))

#cv2.imshow(img_name[0], img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv2.imwrite(f'{img_aug_path}/{save_name}',img)
inserDb = 'INSERT INTO Image_aug(owner,image_augmen) VALUES (%s,%s);'
cursor.execute(inserDb,((user_id,save_name)))
dbconfig.conn.commit()
'''

records = []

#對每張影像作aug
for img_name in cursor:
    print(img_name)
    
    image_name =  list(img_name)[0]
    img = cv2.imread(f'{img_path}/{image_name}')
    save_name = 'aug_' + date_parser() + '_' + image_name
    img = aug_func(img)
    #cv2.imshow('img',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #break
    cv2.imwrite(f'{img_aug_path}/{save_name}',img)
    records.append((user_id,save_name))    

#一次插入多張，用LOOP單張插入無法使用(不知為啥)
inserDb = 'INSERT INTO Image_aug(owner,image_augmen) VALUES (%s,%s);'
cursor = dbconfig.conn.cursor()
cursor.executemany(inserDb,records)
dbconfig.conn.commit()
    
    
# for row in cursor:
#    print(row)

output = json.dumps(result)
#output = str(output)

#sys.stdout.flush()


'''
if __name__=="__main__":
    img = cv2.imread("./test.jpg")
    img = adjust_gamma(img,gamma=1.0)
    cv2.imshow('m',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''
