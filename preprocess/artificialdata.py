#coding=utf-8
import cv2
import os
import random
import  numpy as np
#制作模糊数据
def choose_method(image,method):
    kenel_size=random.randint(5,15)#卷积核大小范围为0~15
    print method
    if kenel_size%2==0:
        kenel_size+=1
    print kenel_size
    if method=='avg_smooth':
        dst = cv2.blur(image,(kenel_size,kenel_size))
    elif method=='gaussian_smooth':
        dst = cv2.GaussianBlur(image,(kenel_size,kenel_size),0)
    elif method=='median_smooth':
        dst = cv2.medianBlur(image,kenel_size)
    elif method=='bilateral_smooth':
        dst=cv2.bilateralFilter(image,kenel_size,kenel_size+50,kenel_size+50)
    elif method=='resize_smooth':
        scale=(image.shape[1]/(2+kenel_size%4),image.shape[0]/(2+kenel_size%4))
        resized_image = cv2.resize(image,scale)
        dst=cv2.resize(resized_image,(image.shape[1],image.shape[0]))
    elif method=='gaussian_noise':
        noise_R=random.uniform(1.5,4.5)
        noise_std=random.uniform(6,22)
        dst=np.random.normal(0, noise_std, size=(image.shape[0],image.shape[1]))

        #dst=np.clip(dst,-10,10)
        #print dst

        dst=np.asarray([dst,dst,dst]).transpose((1,2,0))
        print dst.shape
        #.reshape(image.shape[0],image.shape[1],3)


        dst=cv2.resize(dst,(int(image.shape[0]*noise_R),int(image.shape[1]*noise_R)))
        #print dst
        A=image
        B=np.clip(image+dst[:image.shape[0],:image.shape[1]],0,255)
        C=np.clip(dst[:image.shape[0],:image.shape[1]],0,255)
        image=np.concatenate([A, B,C], 1)
        #cv2.imshow('dst',dst)
        #cv2.waitKey(0)


            #+image

    return image,noise_std,noise_R

def create_blur_data(dataroot):
    ori_dataroot=dataroot+'/'+'ori'
    files=os.listdir(ori_dataroot)
    for f in files:
        dirname=os.path.splitext(f)[0]
        if os.path.exists(os.path.join(dataroot,dirname)) is False:
            os.makedirs(os.path.join(dataroot,dirname))
        image=cv2.imread(ori_dataroot+'/'+f)
        dmethod=['avg_smooth','gaussian_smooth','median_smooth','resize_smooth',
                 'gaussian_noise']
        for d in dmethod:
            newfile_path=os.path.join(dataroot,dirname)+'/'+dirname+'_'+d+'.jpg'
            cv2.imwrite(newfile_path,choose_method(image,d))
def create_blur_data2(datarootA,datarootB):
    files=os.listdir(datarootA)
    for f in files:
        dirname=os.path.splitext(f)[0]
        imageB=cv2.imread(datarootA+'/'+f)

        dmethod=['gaussian_noise']
        for d in dmethod:
            imageA,std,R=choose_method(imageB,d)
            #print imageA
            newfile_pathB=datarootB+'/'+dirname+'_std'+str(std)+'_R'+str(R)+'.jpg'
            cv2.imwrite(newfile_pathB,imageA)
#create_blur_data('../data/batch2_ori')
create_blur_data2('213/00005800','ab')
create_blur_data2('213/00005845','ab')
create_blur_data2('213/00005897','ab')
create_blur_data2('213/00005942','ab')
create_blur_data2('213/00005962','ab')
create_blur_data2('light/origin','ab')


