import numpy as np
import random

def random_noise(whether, image, noise_num):     ##随机噪声
    if whether == True:
        # 参数image：，noise_num：
        img_noise = image.reshape(28, 28)
        # cv2.imshow("src", img)
        rows = 28
        cols = 28
        # 加噪声
        for i in range(noise_num):
            x = np.random.randint(0, rows)#随机生成指定范围的整数
            y = np.random.randint(0, cols)
            img_noise[x, y] = 255
        return img_noise.reshape(1, 784)
    else:
        return image

def sp_noise(whether, image, prob, thresh):    ##给图像加椒盐噪声
    if whether == True:
        ##prob:噪声比例
        image = image.reshape(28, 28)
        output = image.reshape(28, 28)
        thres = 1 - prob
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if random.random() > thresh:
                    rdn = random.random()   #随机生成0-1之间的数字
                    if rdn < prob:          #如果生成的随机数小于噪声比例则将该像素点添加黑点，即椒噪声
                        output[i][j] = 0
                    elif rdn > thres:       #如果生成的随机数大于（1-噪声比例）则将该像素点添加白点，即盐噪声
                        output[i][j] = 255
                    else:
                        output[i][j] = image[i][j]#其他情况像素点不变
        return output.reshape(1, 784)
    else:
        return image

def gauss_noise(whether, image, mean=0, var=0.001):     ##给图像加高斯噪声
    if whether == True:
        ##mean : 均值 
        ##var : 方差越大，噪声越大
        image = image.reshape(28, 28)
        image = np.array(image/255, dtype=float)#将原始图像的像素值进行归一化，除以255使得像素值在0-1之间
        noise = np.random.normal(mean, var ** 0.5, image.shape)#创建一个均值为mean，方差为var呈高斯分布的图像矩阵
        out = image + noise#将噪声和原始图像进行相加得到加噪后的图像
        if out.min() < 0:
            low_clip = -1.
        else:
            low_clip = 0.
        out = np.clip(out, low_clip, 1.0)#clip函数将元素的大小限制在了low_clip和1之间了，小于的用low_clip代替，大于1的用1代替
        out = np.uint8(out*255)#解除归一化，乘以255将加噪后的图像的像素值恢复
        #cv.imshow("gasuss", out)
        ##noise = noise*255
        return out.reshape(1, 784)
    else: 
        return image

def rec_white(whether, image, size, top, left):    ##矩形mask,变成空的
    if whether == True:
        ##将一部分值按规律变成1
        image = image.reshape(28, 28)
        for j in range(top, top + size):
            for k in range(left, left + size):
                image[j][k] = 255
        return image.reshape(1, 784)
    else:
        return image

def rec_black(whether, image, size, top, left):    ##矩形mask,变成空的
    if whether == True:
        ##将一部分值按规律变成1
        image = image.reshape(28, 28)
        for j in range(top, top + size):
            for k in range(left, left + size):
                image[j][k] = 1
        return image.reshape(1, 784)
    else:
        return image