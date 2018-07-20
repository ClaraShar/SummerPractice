# -*- coding:utf-8 -*-

import pymongo

mongo_client = pymongo.MongoClient('192.168.0.90', 27017)
# d = dict((db, [collection for collection in mongo_client[db].collection_names()])
#          for db in mongo_client.list_database_names())
# # print(json.dumps(d))
# print(len(d))

# 1、数据个数
# count = 0
# for db in mongo_client.list_database_names():
#     for collection in mongo_client[db].list_collection_names():
#         for data in mongo_client[db][collection].find():
#             # print(data)
#             count = count+1
# print(count)

# 2、数据字典结构
# for db in mongo_client.list_database_names():
#     for collection in mongo_client[db].list_collection_names():
#         data = mongo_client[db][collection].find_one()
#         key = data.keys()
#         print('key = {}'.format(key))


# 3、查询索引
for db in mongo_client.list_database_names():
    for collection in mongo_client[db].list_collection_names():
        for index in mongo_client[db][collection].list_indexes():
           print(index)
