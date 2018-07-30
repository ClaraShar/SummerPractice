# -*- coding: utf-8 -*- 
import jieba
import re
import os
import math

global words
words = []
global result
total = 0
path = "D:\\实习\\7-27\\document"
global count_bit
###################列表去重####################
def dedupe(items, key=None):
    seen = set()
    for item in items:
        # - 不可哈希值转可哈希值部分(核心)
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


#############读文件，暂存字符串,分词############
def cut_words(file):
    f = open(file, "r", encoding="utf-8")
    temp = f.read()
    st = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。“”？、~@#￥%……&*（）]+", "", temp)
    cut = jieba.cut(st)
    global words
    for i in cut:
        words.append(i)
    del words[0]
    global result
    result = list(dedupe(words, key=lambda x: tuple(x)))
    global total
    total = len(result) # 计算去重后的词数个数
    value = [0]*total # 初始化字典的值
    dic = dict(zip(result, value)) # 将列表转化为字典

    for i in words:
        dic[i] += 1
    return dic


###############计算各词语hash值#############
def hashcode():
    h = [0]*total
    ha = dict(zip(result, h))
    global count_bit
    count_bit = 0
    for i in words:
        ha[i] = []
        b = bin(hash(i))
        b = re.sub("0b", "", b)
        if b.find("-") != -1:
            bit = len(b)
        else:
            bit = len(b)+1
        if bit > count_bit:
            count_bit = bit
        ha[i] = list(str(b))

    for i in words:
        length = len(ha[i])
        if length < count_bit:
            if '-' in ha[i]:
                ha[i].remove('-')
                ha[i].insert(0, '1')
                for j in range(1, count_bit-length+1):
                    ha[i].insert(j, '0')
            else:
                for j in range(count_bit-length):
                    ha[i].insert(j, '0')
        else:
            if '-' in ha[i]:
                ha[i].remove('-')
                ha[i].insert(0, '1')
    return ha


###############计算tf################
def term_frequency(dic):
    n = len(words)
    t = [0]*total
    tf = dict(zip(result, t))
    for a in result:
        tf[a] += dic.get(a)/n
    return tf


###############计算文件总数D################
def count_documents():
    ls = os.listdir(path)
    D = 0
    for i in ls:
        if os.path.isfile(os.path.join(path, i)):
            D += 1
    return D


###########循环计算包含某词语的文件数目###########
def count_word_documents():    
    z = [0]*total
    doc = dict(zip(result, z))
    for b in result:
        d = 0
        files = os.listdir(path)
        for i in files:
            if not os.path.isdir(i):
                f = open(path + "/" + i, "r", encoding="utf-8")
                r = f.read()
                if r.find(b) != -1:
                    d += 1
        doc[b] = d
    return doc


###################计算idf###################
def inverse_document_frequency():
    doc = count_word_documents()
    D = count_documents()        
    c = [0]*total
    idf = dict(zip(result, c))
    for q in result:
        idf[q] = math.log(D/doc[q])# 数据量大的时候取1+
    return idf


##################计算tf-idf#################
def calculate_tf_idf(tf, idf):
    e = [0]*total
    tf_idf = dict(zip(result, e))
    for n in result:
        tf_idf[n] = tf[n]*idf[n]
    return tf_idf


#####################加权####################
def weighting(ha, tf_idf):
    w = [0]*total
    weight = dict(zip(result, w))
    for i in result:
        weight[i] = []
        for b in ha[i]:
            if b == "1":
                weight[i].append(tf_idf[i])
            else:
                weight[i].append(-tf_idf[i])
    return weight


####################合并####################
def merge(weight):
    merge_weight = []
    for i in range(count_bit):
        m = 0
        for j in result:
            m += weight[j][i]
        merge_weight.append(m)
    return merge_weight


###################降维####################
def dimension(merge_weight):
    fp = [-1]*len(merge_weight)
    for i in range(len(merge_weight)):
        if merge_weight[i] > 0:
            fp[i] = 1
        else:
            fp[i] = 0
    return fp


##################程序入口#################
def entrance(file):
    dic = cut_words(file)
    ha = hashcode()
    tf = term_frequency(dic)
    idf = inverse_document_frequency()
    tf_idf = calculate_tf_idf(tf, idf)
    weight = weighting(ha, tf_idf)
    merge_weight = merge(weight)
    fp_list = dimension(merge_weight)
    return fp_list


##################汉明距离#################
def hamming_distance(fp1, fp2):
    dis = 0
    for i in range(len(fp1)):
        r = fp1[i] ^ fp2[i]
        if r == 1:
            dis += 1
    print(dis)

if __name__ == '__main__':
    file1 = 'D:\实习\\7-27\document\\test.txt'
    fp1_list = entrance(file1)
    file2 = 'D:\实习\\7-27\document\\test0.txt'
    fp2_list = entrance(file2)
    hamming_distance(fp1_list, fp2_list)
