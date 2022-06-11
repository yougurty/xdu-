
import numpy as np
from numpy import array
from pyope.ope import OPE, ValueRange
def LoadTxtMethod1(filename):  # 传入形参,txt的名字.
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
    return array(result)
# 读入处理txt文件,返回二维数组，明文和密文
def LoadTxtMethod2(filename):  # 传入形参,txt的名字.
    cipher = OPE(b'long key' * 2, in_range=ValueRange(0, 10000000),
                 out_range=ValueRange(0, 100000000))
    result_m = list()  # 明文点.
    result_c = []
    for line in open(filename):  # 逐行打开文档.
        # line = line.strip()  # 去除这一行的头和尾部空格
        plain_text =line.split(' ' ,1)  # 切片的运算,以逗号为分隔,隔成两个
        plain_text[0] = float( plain_text[0])
        plain_text[1] = float( plain_text[1])
        plain_text_arr =np.array( plain_text)  # 转化数据格式
        result_m.append( plain_text_arr)  # 把第一列数据添加到result序列中

        cipher_text = []
        cipher_text.append(cipher.encrypt(int(plain_text[0] * 1000000)))
        cipher_text.append(cipher.encrypt(int(plain_text[1] * 1000000)))
        cipher_text_arr = np.array(cipher_text)  # 转化数据格式
        result_c.append(cipher_text_arr)
        print("加密" +str(cipher_text_arr[0]) +','+str(cipher_text_arr[1]))
    # result_c= np.array(cipher_text_arr)
    return array(result_m),array(result_c)

def WriteTxt(cipher_txt):
    with open('cipherText.txt', 'a', encoding='utf-8') as f:
        for x in cipher_txt:
            print(type(x))
            strings = str(x[0]) + ' ' + str(x[1])+'\n'
            f.write(strings)
        # f.write(text)

if __name__ == "__main__":
    data1,data2 = LoadTxtMethod2('NE.txt')  # 调用上面数据处理程序
    # data2 = LoadTxtMethod1('NE.txt')
    WriteTxt(data2)                         #加密之后的数据存放于cipherText.txt中

