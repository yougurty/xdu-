import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from sklearn.neighbors import KDTree
# 读入处理txt文件
def LoadTxtMethod2(filename):  # 传入形参,txt的名字.

    result =list()  # 创建要返回的数据.
    for line in open(filename):  # 逐行打开文档.
        # line = line.strip()  # 去除这一行的头和尾部空格
        data =line.split(' ' ,1)  # 切片的运算,以逗号为分隔,隔成两个
        # print('data[0]:' +data[0]+",data[1]"+data[0])
        data[0] = float(data[0])
        data[1] = float(data[1])

        # print(type(data[0]))
        data_float =np.array(data)  # 转化数据格式
        # print(data_float[0])
        result.append(data_float)  # 把第一列数据添加到result序列中
    return result

np.random.seed(0)
# 随机产生150个二维数据
# points = np.random.random((150, 2))
points =  LoadTxtMethod2('NE.txt')
tree = KDTree(points)
point = points[0]
# k近邻发搜索
dists, indices = tree.query([point], k=4)

# q指定半径搜索
indices = tree.query_radius([point], r=0.03)

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.add_patch(Circle(point, 0.2, color='g', fill=False))
X, Y = [p[0] for p in points], [p[1] for p in points]
plt.scatter(X, Y)
plt.scatter([point[0]], [point[1]], c='r')
plt.show()
