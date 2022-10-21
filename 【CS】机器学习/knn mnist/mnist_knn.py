import numpy as np
import matplotlib.pyplot as plt
import time
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from Distance import *              #我的距离计算文件
from pic_mask import *              #我的mask文件
from characterization import *      #我的预处理文件
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

batch_size = 100
path ='./'
train_datasets = datasets.MNIST(root=path,          #选择数据的根目录
                                train = True,       #选择训练集
                                transform = None,   #不考虑使用任何数据预处理
                                download = True)    # 从网络上download图片
test_datasets = datasets.MNIST(root=path,
                               train=False,         #选择测试集
                               transform = None,    #不考虑使用任何数据预处理
                               download=True)

train_loader = DataLoader(train_datasets, batch_size=batch_size, shuffle=True)  # 加载数据
test_loader = DataLoader(test_datasets, batch_size=batch_size, shuffle=True)

x_train = train_loader.dataset.data.numpy()         # 对训练数据处理
y_train = train_loader.dataset.targets.numpy()
# for i in range(len(y_train)):
#     if(y_train[i] == "0"):
#         x_train[i] = deskewing(x_train[i].reshape(784, 1))     #数据集图像校正
mean_image = getXmean(x_train)   # 归一化处理
x_train = centralized(x_train, mean_image)


num_test = 10000        # 对测试数据处理，取前num_test个测试数据
x_test = test_loader.dataset.data[:num_test].numpy()
mean_image = getXmean(x_test)
x_test = centralized(x_test, mean_image)
y_test = test_loader.dataset.targets[:num_test].numpy()

for i in range(60000):
    x_train[i] = random_noise(whether = False, image = x_train[i], noise_num = 364)  # random
    x_train[i] = sp_noise(whether = False, image = x_train[i], prob = 0.5, thresh = 0.5)           # sp
    x_train[i] = gauss_noise(whether = False, image = x_train[i])                          # gauss
    x_train[i] = rec_white(whether = False, image = x_train[i], size = 14, top = 14, left = 14)    # white mask
    x_train[i] = rec_black(whether = True, image = x_train[i], size = 14, top = 14, left = 14)    # black mask

PCA = True
if PCA == True:
    x_train, x_test = PCA_alg(x_train, x_test)     # use PCA in dimension reduction

LDA = False
if LDA == True:
    lda = LinearDiscriminantAnalysis(n_components = 8)
    lda.fit(x_train, y_train)
    x_train = lda.transform(x_train)
    x_test = lda.transform(x_test)

print("train_data:",x_train.shape)
print("train_label:",len(y_train))
print("test_data:",x_test.shape)
print("test_labels:",len(y_test))

k  =  3                    #输出结果
start = time.time()
classifier = Knn()
classifier.fit(x_train[:60000], y_train[:60000])                
y_pred = classifier.predict(k, 'L2', x_test)     #在这里选择要使用的距离公式，"L1", "L2_d", "L2", "L3"
num_correct = np.sum(y_pred == y_test)
# for i in range(len(y_pred)):
#     if(y_pred[i] != y_test[i]):
#         print(str(y_pred[i]) + "," + str(y_test[i]))
accuracy = float(num_correct) / num_test
end = time.time()
duration = end - start
print('Got %d / %d correct when k= %d => accuracy: %f, duration = %f seconds' % (num_correct, num_test, k, accuracy, duration))

