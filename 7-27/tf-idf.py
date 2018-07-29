# -*- coding: utf-8 -*- 
import jieba
import re
import os
import math


words = []
global result
total = 0
path = "/home/clara/文档/SummerPractice/7-27/document"
###################列表去重####################
def dedupe(items, key=None):
    seen = set()
    for item in items:
        # - 不可哈希值转可哈希值部分(核心)
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

###############计算tf################
def tf(dic):
    n = len(words)
    t = [0]*total
    tf = dict(zip(result, t))
    for a in result:
        tf[a] += dic.get(a)/n
    return tf


#############读文件，暂存字符串,分词############
def cut_words():
    file = open('/home/clara/文档/SummerPractice/7-27/document/test.txt', "r", encoding="utf-8")
    temp = file.read()
    str = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。“”？、~@#￥%……&*（）]+", "", temp)
    cut = jieba.cut(str)
    for i in cut:
        words.append(i)
    global result
    result = list(dedupe(words, key=lambda x: tuple(x)))
    global total
    total = len(result) # 计算去重后的词数个数
    value = [0]*total # 初始化字典的值
    dic = dict(zip(result, value)) # 将列表转化为字典

    for i in words:
        dic[i] += 1
    return dic


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
    # print(d)
    # print(doc.items())


###################计算idf###################
def idf():
    doc = count_word_documents()
    D = count_documents()        
    c = [0]*total
    idf = dict(zip(result, c))
    for q in result:
        idf[q] = math.log(D/doc[q])# 数据量打的时候取1+
    return idf

##################计算tf-idf#################
def tf_idf(tf, idf):
    e = [0]*total
    tf_idf = dict(zip(result, e))
    for n in result:
        tf_idf[n] = tf[n]*idf[n]
    print(tf_idf.items())


if __name__ == '__main__':
    dic = cut_words()
    tf = tf(dic)
    idf = idf()
    tf_idf(tf, idf)

