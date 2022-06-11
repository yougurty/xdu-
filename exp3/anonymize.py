import copy
import numpy as np
import pandas as pd
from basic_mondrian import *
import csv #调用数据保存文件

if __name__ == '__main__':
    # K = int(input('input K:'))
    K = 4
    data_path = 'data/adult.csv'
    hierarchies_paths = ['data/hierarchies', 'data/hierarchies_gen']
    result_path = f'results/{K}-anonymity.csv'
    os.makedirs('results', exist_ok=True)

    print("Sdfsf")
    data = pd.read_csv(data_path, delimiter=';')
    ATT_NAMES = list(data.columns)
    QI_INDEX = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    SA_INDEX = [14]
    QI_NAMES = list(np.array(ATT_NAMES)[QI_INDEX])

    ATT_TREES = read_tree(hierarchies_paths, ATT_NAMES, QI_INDEX)
    raw_data, header = read_raw(data_path)

    anon_data,raw_data = mondrian(
        ATT_TREES, reorder_columns(copy.deepcopy(raw_data), QI_INDEX),
        K, len(QI_INDEX), len(SA_INDEX))
    # print(type(anon_data))
    # print(anon_data)
    column = ['age', 'workclass','fnlwgt', 'education','education-num','marital-status','occupation','relationship','race','sex' ,'capital-gain','capital-loss','hours-per-week','native-country','salary-class']  # 列表头名称
    test = pd.DataFrame (columns=column, data=anon_data)  # 将数据放进表格
    test.to_csv('4-Anonymize.csv')  # 数据存入csv,存储位置及文件名称

    # column = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
    #           'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
    #           'salary-class']  # 列表头名称
    # test = pd.DataFrame(columns=column, data=rawdata)  # 将数据放进表格
    # test.to_csv('rawdata.csv')  # 数据存入csv,存储位置及文件名称

    nodes_count = write_anon(result_path, anon_data, raw_data, header)