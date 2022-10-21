import numpy as np

class Knn:
    def __init__(self):
        pass

    def fit(self, X_train, Y_train):
        self.Xtr = X_train  #image
        self.Ytr = Y_train  #label

    def predict(self, k, dis, X_test):
        # assert dis == 'E' or dis == 'M','dis must E or M，E代表欧拉距离，M代表曼哈顿距离'
        num_test = X_test.shape[0]  #read the number of testing set
        label_list = []     #initialization

        if dis == 'L1':       # 使用曼哈顿公式进行度量
            for j in range(num_test):
                distances = np.absolute(np.sum(np.absolute((self.Xtr - np.tile(X_test[j], (self.Xtr.shape[0], 1)))), axis=1))                                                
                nearest_k = np.argsort(distances)
                topK = nearest_k[:k]
                class_count = {}
                for i in topK:
                    class_count[self.Ytr[i]] = class_count.get(self.Ytr[i], 0) + 1
                sorted_class_count = sorted(class_count.items(), key=lambda elem: elem[1], reverse=True)
                label_list.append(sorted_class_count[0][0])
            return np.array(label_list)

        if dis == 'L2_d':       # 使用欧拉公式作为距离测量,使用距离超参数
            for j in range(num_test):
                distances = np.sqrt(np.sum(
                                    (
                                        (self.Xtr - np.tile
                                                    (X_test[j], (self.Xtr.shape[0], 1)        #np.tile：将测试点复制出与x_test同样数量多个，组成一个差值矩阵
                                                    )
                                        )
                                    ) ** 2, axis=1))    
                nearest_k = np.argsort(distances)       #对distance排序，nearest_k存距离
                topK = nearest_k[:k]                    #topK：存距离最小的k个距离
                class_count = {}
                distance_count = {}
                for i in topK:
                    #class_count[self.Ytr[i]] = class_count.get(self.Ytr[i], 0) + 1      #如果classcount里没有当前Y值，则返回0，否则在当前值+1
                    distance_count[self.Ytr[i]] = class_count.get(self.Ytr[i], 0) + (1/distances[self.Ytr[i]])     #如果distancecount里没有Y值，则返回0，否则在当前值+1
                #sorted_class_count = sorted(class_count.items(), key=lambda elem: elem[1], reverse=True)  
                                    #sorted(iterable, cmp = None, key = None, reverse = false)  
                                    #cmp:比较的函数，这个具有两个参数，参数的值都是从可迭代对象中取出，大于则返回1，小于则返回-1，等于则返回0。
                                    #key:主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序
                                    #reverse:true,降序
                                    #dict.items()返回可遍历的（键，值）
                                    #lambda [arg1 [,arg2,.....argn]]:expression，相当于一个自定义函数，lambda 参数：返回值
                                    #elem: list.sort必须接收一个参数作为排序依据，这个参数必须是一个接受一个位置参数的callable对象，例如拥有一个参数的函数。sort方法会调用此函数并逐一传递列表中的元素作为此函数的参数，然后接收函数的返回值作为该元素的权重
                sorted_ditance_count = sorted(distance_count.items(), key = lambda elem: elem[1], reverse = True)
                #label_list.append(sorted_class_count[0][0])     #
                label_list.append(sorted_ditance_count[0][0])
            return np.array(label_list)

        if dis == 'L2':       # 使用欧拉公式作为距离测量
            #对每一个测试点，将测试点复制形成与训练集维数相同的矩阵，分别得到到每一个训练点的距离，按行相加（每一个维度的距离相加后再开平方）
            #因为行是一个点的所有维度
            for j in range(num_test):
                distances = np.sqrt(np.sum(((self.Xtr - np.tile(X_test[j], (self.Xtr.shape[0], 1)))) ** 2, axis=1))
                nearest_k = np.argsort(distances)
                topK = nearest_k[:k]
                class_count = {}
                for i in topK:
                    class_count[self.Ytr[i]] = class_count.get(self.Ytr[i], 0) + 1
                sorted_class_count = sorted(class_count.items(), key=lambda elem: elem[1], reverse=True)
                label_list.append(sorted_class_count[0][0])
            return np.array(label_list)

        if dis == 'L3':       # 使用L3距离作为距离测量（闵可夫斯基距离，当p=3时）, L3的计算方法为立方和的立方根
            for j in range(num_test):
                distances = np.absolute(np.cbrt(np.sum(((np.absolute(self.Xtr - np.tile(X_test[j], (self.Xtr.shape[0], 1))))) ** 3, axis=1)))
                nearest_k = np.argsort(distances)
                topK = nearest_k[:k]
                class_count = {}
                for i in topK:
                    class_count[self.Ytr[i]] = class_count.get(self.Ytr[i], 0) + 1
                sorted_class_count = sorted(class_count.items(), key=lambda elem: elem[1], reverse=True)
                label_list.append(sorted_class_count[0][0])
            return np.array(label_list)