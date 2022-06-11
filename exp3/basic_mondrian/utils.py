# -*- coding: utf-8 -*-

import csv
import os

#读取原始数据，返回数据和表
def read_raw(path, delimiter=';'):
    data = []
    with open(os.path.join(path)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        header = next(csv_reader)

        for row in csv_reader:
            data.append(row)

    return data, header


def reorder_columns(data, qi_index):
    res = []
    for row in data:
        qi = [elem for i, elem in enumerate(row) if i in qi_index]
        non_qi = [elem for i, elem in enumerate(row) if i not in qi_index]
        res.append([*qi, *non_qi])
    return res


def restore_column_order(data, qi_index):
    res = []
    for row in data:
        new_row = row[len(qi_index):]
        for i, elem in zip(qi_index, row[:len(qi_index)]):
            new_row.insert(i, elem)
        res.append(new_row)
    return res

# 最后的结果写到/results中
def write_anon(path, anon_data, raw_data, header, delimiter=';'):
    f_anon = open(os.path.join(path, 'result.csv'), 'w', newline='')
    f_raw = open(os.path.join(path, 'raw.csv'), 'w', newline='')
    anon_writer = csv.writer(f_anon, delimiter=delimiter)
    raw_writer = csv.writer(f_raw, delimiter=delimiter)
    anon_writer.writerow(header)
    anon_writer.writerows(anon_data)
    raw_writer.writerow(header)
    raw_writer.writerows(raw_data)
