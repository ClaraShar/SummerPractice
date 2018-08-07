# -*- coding: utf-8 -*-
import jieba
import re
import datetime
import math
import hashlib
import pymongo
from bson import ObjectId

global words
words = []
global result
total = 0

global mongo_client
global db
global collection

mongo_client = pymongo.MongoClient('192.168.0.34', 22222)
db = mongo_client["中国家电网(新闻)"]
collection = db["卫浴"]

###################访问数据库##################
def access_mongo(id):
    global collection
    x = collection.find_one({"_id": id}) # id有问题
    txt = x.get('文本内容')
    dic = cut_words(txt)
    return dic

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
def cut_words(txt):
    st = re.sub(r"[\s\n+\.\!\/_,;$%^*()\"\'——！，。：；？“”！、~@#￥%……&*（）的之了和为到从就里是才再也着并而去能]", "", txt)
    cut = jieba.cut(st)
    global words
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


###############变成128位二进制##############
def to_bin(b):
    lis = []
    num = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "a": "1010",
        "b": "1011",
        "c": "1100",
        "d": "1101",
        "e": "1110",
        "f": "1111"}
    for c in b:
        s = num[c]
        lis.append(s)
    lis = "".join(lis)
    lis = list(lis)
    return lis

###############计算各词语hash值#############
def hashcode():
    h = [0]*total
    ha = dict(zip(result, h))

    for i in words:
        ha[i] = []
        b = hashlib.md5(i.encode("utf-8")).hexdigest()# b是32为16进制字符串
        ha[i] = to_bin(b)
    return ha


###############计算tf################
def term_frequency(dic):
    n = len(words)
    t = [0]*total
    tf = dict(zip(result, t))
    for a in result:
        tf[a] += dic.get(a)/n
    return tf


###############计算数据库记录总数D################
def count_documents():
    global mongo_client
    D = 0
    for database in mongo_client.list_database_names():
        for col in mongo_client[database].list_collection_names():
            D += mongo_client[database][col].find().count()
    return D


###########循环计算包含某词语的文件数目###########
def count_word_documents():
    global mongo_client
    z = [0]*total
    doc = dict(zip(result, z))
    for w in result:
        d = 0
        for database in mongo_client.list_database_names():
            for col in mongo_client[database].list_collection_names():
                for x in mongo_client[database][col].find({"文本内容": {"$regex": w}}):
                    if x:
                        d += 1
        doc[w] = d
    return doc


###################计算idf###################
def inverse_document_frequency():
    doc = count_word_documents()
    D = count_documents()
    c = [0]*total
    idf = dict(zip(result, c))
    for q in result:
        if doc[q] == 0:
            idf[q] = 0
        else:
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
    for i in range(128):
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
def entrance(id):
    dic = access_mongo(id)
    ha = hashcode()
    tf = term_frequency(dic)
    idf = inverse_document_frequency()
    tf_idf = calculate_tf_idf(tf, idf)
    weight = weighting(ha, tf_idf)
    merge_weight = merge(weight)
    fp_list = dimension(merge_weight)
    print(fp_list)
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
    starttime = datetime.datetime.now()
    id1 = ObjectId("5b6184bffea65d2f88a96c0f")
    fp1_list = entrance(id1)
    id2 = ObjectId("5b6184bffea65d2f88a96c10")
    fp2_list = entrance(id2)
    hamming_distance(fp1_list, fp2_list)
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
