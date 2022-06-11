# -*- coding: utf-8 -*-

"""
main module of basic Mondrian
"""
import copy
import pdb
import time
from functools import cmp_to_key

from tqdm import tqdm

QI_LEN = 8
SA_LEN = []
GL_K = 0
RESULT = []
ATT_TREES = []
QI_RANGE = []


def cmp(a, b):
    return (a > b) - (a < b)


def cmp_str(element1, element2):
    """compare number in str format correctley
    """
    return cmp(float(element1), float(element2))


class Partition(object):

    """Class for Group, which is used to keep records
    Store tree node in instances.
    self.member: records in group
    self.width: width of this partition on each domain. For categoric attribute, it equal
    the number of leaf node, for numeric attribute, it equal to number range
    self.middle: save the generalization result of this partition
    self.allow: 0 donate that not allow to split, 1 donate can be split
    """

    def __init__(self, data, width, middle):
        """
        initialize with data, width and middle
        """
        self.member = list(data)
        self.width = list(width)
        self.middle = list(middle)
        self.allow = [1] * QI_LEN
        self.allow[2] = 0

    def __len__(self):
        """
        return the number of records in partition
        """
        return len(self.member)


def get_normalized_width(partition, index):
    """
    return Normalized width of partition
    similar to NCP
    """
    width = partition.width[index]
    return width * 1.0 / QI_RANGE[index]

#选择某个维度，列进行
def choose_dimension(partition):
    """
    chooss dim with largest normlized Width
    return dim index.
    """
    max_width = -1
    max_dim = -1
    for i in range(QI_LEN):
        if partition.allow[i] == 0:
            continue
        normWidth = get_normalized_width(partition, i)
        if normWidth > max_width:
            max_width = normWidth
            max_dim = i
    if max_width > 1:
        print("Error: max_width > 1")
        pdb.set_trace()
    if max_dim == -1:
        print("cannot find the max dim")
        pdb.set_trace()
    return max_dim


# 拆分分区，将记录分发到不同的子分区
def split_partition(partition, dim):
    """
    split partition and distribute records to different sub-partitions
    """
    pwidth = partition.width
    pmiddle = partition.middle

    sub_partitions = []
    # categoric attributes
    splitVal = ATT_TREES[dim][partition.middle[dim]]
    sub_node = [t for t in splitVal.child]
    sub_groups = []
    for i in range(len(sub_node)):
        sub_groups.append([])
    if len(sub_groups) == 0:
        # split is not necessary
        return []
    for temp in partition.member:
        qid_value = temp[dim]
        for i, node in enumerate(sub_node):
            try:
                node.cover[qid_value]
                sub_groups[i].append(temp)
                break
            except KeyError:
                continue
        else:
            print("Generalization hierarchy error!: " + qid_value)
    flag = True
    for index, sub_group in enumerate(sub_groups):
        if len(sub_group) == 0:
            continue
        elif GL_K != 0:
            if len(sub_group) < GL_K:
                flag = False
                break
    if flag:
        for i, sub_group in enumerate(sub_groups):
            if len(sub_group) == 0:
                continue
            wtemp = pwidth[:]
            mtemp = pmiddle[:]
            wtemp[dim] = len(sub_node[i])
            mtemp[dim] = sub_node[i].value
            sub_partitions.append(Partition(sub_group, wtemp, mtemp))
    return sub_partitions

# 递归分区组，直到不允许为止
def anonymize(partition):
    """
    Main procedure of Half_Partition.
    recursively partition groups until not allowable.
    """
    if check_splitable(partition) is False:
        RESULT.append(partition)            # 不能再细分了，就存到result中
        return
    # Choose dim
    dim = choose_dimension(partition)
    if dim == -1:
        print("Error: dim=-1")
        pdb.set_trace()
    sub_partitions = split_partition(partition, dim)
    if len(sub_partitions) == 0:
        partition.allow[dim] = 0
        anonymize(partition)
    else:
        for sub_p in sub_partitions:
            anonymize(sub_p)

# 检查是否可以在满足k-匿名的情况下进一步分割分区。
def check_splitable(partition):
    """
    Check if the partition can be further splited while satisfying k-anonymity.
    """
    temp = sum(partition.allow)
    if temp == 0:
        return False
    return True

# k匿名的蒙德里安法

def mondrian(att_trees, data, k, qi_len, sa_len):
    """
    basic Mondrian for k-anonymity.
    This fuction support both numeric values and categoric values.
    For numeric values, each iterator is a mean split.
    For categoric values, each iterator is a split on GH.
    The final result is returned in 2-dimensional list.
    """
    global GL_K, RESULT, QI_LEN, ATT_TREES, QI_RANGE, SA_LEN
    ATT_TREES = att_trees
    QI_LEN = qi_len
    SA_LEN = sa_len
    GL_K = k

    results = []
    raw_results = []
    middle = []
    wtemp = []
    for i in range(QI_LEN):
        QI_RANGE.append(len(ATT_TREES[i]['*']))
        wtemp.append(len(ATT_TREES[i]['*']))
        middle.append('*')
    whole_partition = Partition(data, wtemp, middle)
    anonymize(whole_partition)
    for partition in RESULT:
        raw_results.extend(copy.deepcopy(partition.member))
        temp = partition.middle
        for i in range(len(partition)):
            temp_for_SA = []
            for s in range(len(partition.member[i]) - SA_LEN, len(partition.member[i])):
                temp_for_SA = temp_for_SA + [partition.member[i][s]]
            results.append(temp + temp_for_SA)
    return results, raw_results
