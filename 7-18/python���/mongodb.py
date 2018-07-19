# -*- coding:utf-8 -*-

import pymongo

# 1.连接数据库服务器,获取客户端对象
mongo_client = pymongo.MongoClient('192.168.0.90', 27017)


# 2.获取数据库对象
db = mongo_client.liulutest

# 3.获取集合对象
my_collection = db["住建部(诚信数据)"]

# 查询文档个数
# cursor = my_collection.find()
# print(cursor.count())   # 获取文档个数
# print(my_collection.estimated_document_count())
# for item in cursor:
#     print(item)

# 打印数据
'''
data = my_collection.find()
# print(data)
for i in data:
    print(i)
# print(data)
'''

# 打印字典结构
# for key in my_collection.keys():
#    print('key = {}'.format(key))

# 打印索引
# index = my_collection.indexes.find()
# index = my_collection.getIndexes()


index = my_collection.index_information()
for i in index:
    print(i)

# print(index)