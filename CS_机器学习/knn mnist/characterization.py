import numpy as np
from sklearn.decomposition import PCA
import cv2

def getXmean(x_train):
    x_train = np.reshape(x_train,
                         (x_train.shape[0], -1))  # 将28*28像素展开成一个一维的行向量
    mean_image = np.mean(x_train, axis=0)  # 求每一列均值。即求所有图片每一个像素上的平均值
    return mean_image

def centralized(x_test, mean_image):
    x_test = np.reshape(x_test, (x_test.shape[0], -1))
    x_test = x_test.astype(np.float)
    x_test -= mean_image  #减去平均值，实现均一化。
    return x_test

def PCA_alg(train_data, test_data):
    pca = PCA(n_components=60)  ##在这里修改提取多少特征
    pca.fit(
        train_data)  #fit PCA with training data instead of the whole dataset
    train_data_pca = pca.transform(train_data)
    test_data_pca = pca.transform(test_data)
    print("training data shape after PCA:", train_data_pca.shape)
    print("testing data shape after PCA:", test_data_pca.shape)
    return train_data_pca, test_data_pca

def deskewing(img,par = 'cubic'): 	## De-Skew the Images 
	print('De-skewing Images..........')
	deskew_img = np.zeros((img.shape[0], img.shape[1]))
	SZ = int(np.sqrt(img.shape[1]))
	for i in np.arange(img.shape[0]):
		gray = img[i,:].reshape(SZ,SZ)
		gray = gray.astype(np.uint8)
		m = cv2.moments(gray)
		if abs(m['mu02']) < 1e-2:
			# no deskewing needed. 
			deskew_img[i] =  gray.flatten()
			continue
		# Calculate skew based on central momemts. 
		skew = m['mu11']/m['mu02']
		# Calculate affine transform to correct skewness. 
		M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
		# Apply affine transform
		if par == 'cubic':
			gray = cv2.warpAffine(gray, M, (SZ, SZ), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_CUBIC)
		else:
			gray = cv2.warpAffine(gray, M, (SZ, SZ), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
		deskew_img[i] =  gray.flatten()
	return deskew_img