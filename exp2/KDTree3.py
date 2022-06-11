import numpy as np
from numpy import array
from pyope.ope import OPE, ValueRange

#创建类，用于保存结点的值，左右子树，以及用于划分左右子树的切分轴
class decisionnode:
    def __init__(self,value=None,col=None,rb=None,lb=None):
        self.value=value        # 点
        self.col=col            #切分的维度
        self.rb=rb             # 右子树
        self.lb=lb              # 左子树

def LoadTxtMethod(filename):  # 传入形参,txt的名字.

    result =list()  # 创建要返回的数据.
    for line in open(filename):  # 逐行打开文档.
        # line = line.strip()  # 去除这一行的头和尾部空格
        data =line.split(' ' ,1)  # 切片的运算,以逗号为分隔,隔成两个
        # print('data[0]:' +data[0]+",data[1]"+data[0])
        data[0] = float(data[0])
        data[1] = float(data[1])

        data_float =np.array(data)  # 转化数据格式
        result.append(data_float)  # 把第一列数据添加到result序列中
    return array(result)

# 切分点为坐标轴上的中值，求一个序列的中值
def median(x):
    n=len(x)
    x=list(x)
    x_order=sorted(x)
    return x_order[n//2],x.index(x_order[n//2])

#以j列的中值划分数据，左小右大，j=节点深度%列数，列数这里是2
def buildtree(x,j=0):
    rb=[]
    lb=[]
    m,n=x.shape
    if m==0: return None
    edge,row=median(x[:,j].copy())
    for i in range(m):
        if x[i][j]>edge:
            rb.append(i)
        if x[i][j]<edge:
            lb.append(i)
    rb_x=x[rb,:]
    lb_x=x[lb,:]
    rightBranch=buildtree(rb_x,(j+1)%n)
    leftBranch=buildtree(lb_x,(j+1)%n)
    return decisionnode(x[row,:],j,rightBranch,leftBranch)

# 搜索树：输出目标点的近邻点
def traveltree(node,aim):
    global pointlist            # 存储排序后的k近邻点和对应距离
    if node==None: return
    col=node.col
    if aim[col]>node.value[col]:    # 顺着树进行搜索，分类
        traveltree(node.rb,aim)
    if aim[col]<node.value[col]:
        traveltree(node.lb,aim)
    dis=dist(node.value,aim)
    if len(knears)<k:               # k是输入的要查询的个数，前k个点就是目标点x的k近邻
        knears.setdefault(tuple(node.value.tolist()),dis)    # 列表不能作为字典的键
        pointlist=sorted(knears.items(),key=lambda item: item[1],reverse=True)
    elif dis<=pointlist[0][1]:
        knears.setdefault(tuple(node.value.tolist()),dis)
        pointlist=sorted(knears.items(),key=lambda item: item[1],reverse=True)
    if node.rb!=None or node.lb!=None:
        # 对于父节点来说，如果目标点与其切分轴之间的距离不大于字典中各结点所对应距离的的最大值，便需要访问该父节点的另一个子节点
        if abs(aim[node.col] - node.value[node.col]) < pointlist[0][1]:
            if aim[node.col]<node.value[node.col]:
                traveltree(node.rb,aim)
            if aim[node.col]>node.value[node.col]:
                traveltree(node.lb,aim)
    return pointlist

def dist(x1, x2): #欧式距离的计算
    return ((np.array(x1) - np.array(x2)) ** 2).sum() ** 0.5


cipher = OPE(b'long key' * 2, in_range=ValueRange(0, 10000000),
                 out_range=ValueRange(0, 100000000))
# 保序加密
# 输入给的点，输出调用pyope库加密的点
def encryption(point):

    point[0] = float(point[0])
    point[1] = float(point[1])          #把array中的点转化为float类型
    en_point = []
    en_point.append(cipher.encrypt(int(point[0] * 1000000)))
    en_point.append(cipher.encrypt(int(point[1] * 1000000)))
    en_point_arr = np.array(en_point)  # 转化数据格式

    return en_point_arr
#保序解密
def decryption(point):
    point[0] = int(point[0])
    point[1] = int(point[1])
    de_point = []
    de_point.append(cipher.decrypt(point[0])/1000000)
    de_point.append(cipher.decrypt(point[1])/1000000)
    # print(de_point)
    de_point_arr = np.array(de_point)

    return de_point_arr

if __name__ == "__main__":

    tmp = input('请输入目标点,目标点的格式为(x,y)\n')
    tmp = tmp.split(',')
    point_tmp = encryption(tmp)  # 对目标点进行加密
    print("输入的点为 ", tmp)
    aim = []
    for num in point_tmp:
        aim.append(num)

    knears={}
    k = int(input('需要查询的邻近点的个数\n'))
    global pointlist
    pointlist = []
    file = 'cipherText.txt'
    data_c = LoadTxtMethod(file)
    print('共有'+str(len(data_c))+'条数据')
    tree = buildtree(data_c)            #构建KD tree

    pointlist = traveltree(tree , aim)          #对目标点进行检索
    i = 1
    for point in pointlist[-k:]:            # 里面存的有点，和欧式距离
         x = []
         x.append(point[0][0])
         x.append(point[0][1])
         de_point = decryption(x)
         print("-------------第"+str(i) + "条检索数据------------")
         print("检索得到的点为 " , de_point)
         print("欧式距离为：", dist(tmp , de_point))
         i = i+1