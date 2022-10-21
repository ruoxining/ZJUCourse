from re import A
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def historium(price):
    # data processing
    price = list(price)
    price.sort()
    block = []   # calculate each block
    for i in range(price[-1]//100000 + 1):
        block.append(0)
    for i in price:
        block[i//100000] += 1

    # plot
    plt.figure(figsize=(8, 6), dpi=80)  # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
    plt.subplot(1, 1, 1)    # 再创建一个规格为 1 x 1 的子图
    N = len(block)          # 柱子总数
    index = np.arange(N)    # 包含每个柱子下标的序列
    width = 0.5            # 柱子的宽度
    p2 = plt.bar(index, block, width, label="number",
                 color="#00ffcc")   # 绘制柱状图
    plt.xlabel('SalePrice')    # 设置横轴标签
    plt.ylabel('number')  # 设置纵轴标签
    plt.title('Sale Price')   # 添加标题
    plt.xticks(index, ('0-10w', '10w-20w', '20w-30w', '30w-40w',
               '40w-50w', '50w-60w', '60w-70w', '70w-80w'))   # 添加纵横轴的刻度
    plt.yticks(np.arange(0, 1000, 100))
    plt.legend(loc="upper right")   # 添加图例
    plt.show()


def scatter(price_ori, area_ori):
    price = []
    area = []
    for i in range(len(price_ori)):
        if price_ori[i] != 0 and area_ori[i] != 0:
            price.append(price_ori[i])
            area.append(area_ori[i])

    plt.title("Price ~ Area Scartter Diagram")
    plt.xlim(xmax=1100, xmin=100)
    plt.ylim(ymax=800000, ymin=0)
    plt.xlabel("area")
    plt.ylabel("price")
    plt.plot(area, price, '.', color='#00ffcc')
    plt.show()


def boxplot(price, label):
    price = list(price)
    label = list(label)
    type = [[], [], [], [], []]
    for i in range(len(label)):
        if label[i] == '1Fam':
            type[0].append(price[i])
        if label[i] == '2fmCon':
            type[1].append(price[i])
        if label[i] == 'Duplex':
            type[2].append(price[i])
        if label[i] == 'TwnhsE':
            type[3].append(price[i])
        if label[i] == 'Twnhs':
            type[4].append(price[i])

    labels = ['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs']
    plt.title("Price ~ Type Boxplot")
    plt.grid(True)  # 显示网格
    plt.boxplot(type,
                medianprops={'color': 'red', 'linewidth': '1.5'},
                meanline=True,
                showmeans=True,
                meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1.5'},
                flierprops={"marker": ".",
                            "markerfacecolor": "#00ffcc", "markersize": 10},
                labels=labels)
    plt.yticks(np.arange(0, 800000, 100000))
    plt.show()


# read data
df = pd.read_csv(
    "/Users/minervaning/Desktop/DataMining/house-prices-advanced-regression-techniques/train.csv")

historium(df['SalePrice'])
scatter(df['SalePrice'], df['GarageArea'])
boxplot(df['SalePrice'], df['BldgType'])
