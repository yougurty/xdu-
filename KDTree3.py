import numpy as np
from numpy import array
from pyope.ope import OPE, ValueRange

class decisionnode:
    def __init__(self,value=None,col=None,rb=None,lb=None):
        self.value=value
        self.col=col
        self.rb=rb
        self.lb=lb
# # #读取数据并将数据转换为矩阵形式
# def readdata(filename):
#     data=open(filename).readlines()
#     x=[]
#     for line in data:
#         line=line.strip().split('\t')
#         x_i=[]
#         for num in line:
#             num=float(num)
#             x_i.append(num)
#         x.append(x_i)
#     x=array(x)
#     return x
# # 读入处理txt文件
# def LoadTxtMethod2(filename):  # 传入形参,txt的名字.
#
#     result =list()  # 创建要返回的数据.
#     for line in open(filename):  # 逐行打开文档.
#         # line = line.strip()  # 去除这一行的头和尾部空格
#         data =line.split(' ' ,1)  # 切片的运算,以逗号为分隔,隔成两个
#         # print('data[0]:' +data[0]+",data[1]"+data[0])
#         data[0] = float(data[0])
#         data[1] = float(data[1])
#
#         # print(type(data[0]))
#         data_float =np.array(data)  # 转化数据格式
#         # print(data_float[0])
#         result.append(data_float)  # 把第一列数据添加到result序列中
#     return array(result)

# 读入处理txt文件,返回二维数组，明文和密文
# def LoadTxtMethod2(filename):  # 传入形参,txt的名字.
#     cipher = OPE(b'long key' * 2, in_range=ValueRange(0, 10000000),
#                  out_range=ValueRange(0, 100000000))
#     result_m = list()  # 明文点.
#     cipher_text_arr = []
#     for line in open(filename):  # 逐行打开文档.
#         # line = line.strip()  # 去除这一行的头和尾部空格
#         plain_text =line.split(' ' ,1)  # 切片的运算,以逗号为分隔,隔成两个
#         # print('data[0]:' +data[0]+",data[1]"+data[0])
#         plain_text[0] = float( plain_text[0])
#         plain_text[1] = float( plain_text[1])
#         plain_text_arr =np.array( plain_text)  # 转化数据格式
#         result_m.append( plain_text_arr)  # 把第一列数据添加到result序列中
#         cipher_text = []
#         cipher_text.append(cipher.encrypt(int(plain_text[0] * 1000000)))
#         cipher_text.append(cipher.encrypt(int(plain_text[1] * 1000000)))
#         # print(cipher_text)
#         cipher_text_arr.append(cipher_text)
#     result_c= np.array(cipher_text_arr)
#     return array(result_m),result_c

def median(x):
    n=len(x)
    x=list(x)
    x_order=sorted(x)
    return x_order[n//2],x.index(x_order[n//2])

#以j列的中值划分数据，左小右大，j=节点深度%列数
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

#搜索树：输出目标点的近邻点
def traveltree(node,aim):
    global pointlist  #存储排序后的k近邻点和对应距离
    if node==None: return
    col=node.col
    if aim[col]>node.value[col]:
        traveltree(node.rb,aim)
    if aim[col]<node.value[col]:
        traveltree(node.lb,aim)
    dis=dist(node.value,aim)
    if len(knears)<k:
        knears.setdefault(tuple(node.value.tolist()),dis)#列表不能作为字典的键
        pointlist=sorted(knears.items(),key=lambda item: item[1],reverse=True)
    elif dis<=pointlist[0][1]:
        knears.setdefault(tuple(node.value.tolist()),dis)
        pointlist=sorted(knears.items(),key=lambda item: item[1],reverse=True)
    if node.rb!=None or node.lb!=None:
        if abs(aim[node.col] - node.value[node.col]) < pointlist[0][1]:
            if aim[node.col]<node.value[node.col]:
                traveltree(node.rb,aim)
            if aim[node.col]>node.value[node.col]:
                traveltree(node.lb,aim)
    return pointlist
def dist(x1, x2): #欧式距离的计算
    return ((np.array(x1) - np.array(x2)) ** 2).sum() ** 0.5

knears={}
k=int(input('请输入k的值'))
if k<2: print('k不能是1')
global pointlist
pointlist=[]
file='NE.txt'
# data_m, data_c=LoadTxtMethod2(file)
data_c=LoadTxtMethod2(file)
print(len(data_c))
tree=buildtree(data_c)
tmp=input('请输入目标点')
tmp=tmp.split(',')
aim=[]
for num in tmp:
     num=float(num)
     aim.append(num)
aim=tuple(aim)
pointlist=traveltree(tree,aim)
for point in pointlist[-k:]:
     print(point)