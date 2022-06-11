# -*- coding: utf-8 -*-

import os
import pickle
from functools import cmp_to_key

from .gentree import GenTree


def cmp(a, b):
    return (a > b) - (a < b)


def cmp_str(element1, element2):
    """compare number in str format correctley
    """
    return cmp(float(element1), float(element2))


def read_data(path, dataset, ATT_NAMES, QI_INDEX, IS_CAT, SA_INDEX):
    """
    read microda for *.txt and return read data
    """
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    delimiter = ';'
    for i in range(QI_num):
        numeric_dict.append(dict())
    # or categorical attributes in intuitive order
    # here, we use the appear number
    with open(os.path.join(path, dataset + '.csv')) as data_file:
        next(data_file)
        for line in data_file:
            line = line.strip()
            # remove double spaces
            line = line.replace(' ', '')
            temp = line.split(delimiter)
            ltemp = []
            for i in range(QI_num):
                index = QI_INDEX[i]
                if IS_CAT[i] is False:
                    try:
                        numeric_dict[i][temp[index]] += 1
                    except KeyError:
                        numeric_dict[i][temp[index]] = 1
                ltemp.append(temp[index])
            for i in SA_INDEX:
                ltemp.append(temp[i])
            data.append(ltemp)
    # pickle numeric attributes and get NumRange
    for i in range(QI_num):
        if IS_CAT[i] is False:
            with open(os.path.join(path, dataset + '_' + ATT_NAMES[QI_INDEX[i]] + '_static.pickle'), 'wb') as static_file:
                sort_value = list(numeric_dict[i].keys())
                sort_value.sort(key=cmp_to_key(cmp_str))
                pickle.dump((numeric_dict[i], sort_value), static_file)
    return data

# 把树结构读进来。分别是/hierarchies和/hierarchies_gen
def read_tree(paths, ATT_NAMES, QI_INDEX):
    """read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(ATT_NAMES[t])
    for i in range(len(att_names)):
        att_trees.append(read_tree_file(paths, att_names[i]))
    return att_trees


def read_tree_file(paths, treename):
    """read tree data from treename
    """
    att_tree = {}
    prefix = os.path.join(paths[0], 'adult' + '_hierarchy_')
    prefix_gen = os.path.join(paths[1], 'adult' + '_hierarchy_')
    postfix = ".csv"

    filename = prefix + treename + postfix
    if not os.path.exists(filename):
        filename = prefix_gen + treename + postfix

    with open(filename) as treefile:
        att_tree['*'] = GenTree('*')
        for line in treefile:
            # delete \n
            if len(line) <= 1:
                break
            line = line.strip()
            temp = line.split(';')
            # copy temp
            temp.reverse()
            for i, t in enumerate(temp):
                isleaf = False
                if i == len(temp) - 1:
                    isleaf = True

                # try and except is more efficient than 'in'
                try:
                    att_tree[t]
                except KeyError:
                    att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
    return att_tree
