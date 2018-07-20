# -*- coding:utf-8 -*-
import pymongo
from bson import ObjectId

mongo_client = pymongo.MongoClient('192.168.0.144', 22222)
db = mongo_client["21经济网(新闻)"]
my_collection = db["投资通-公告快递"]

# def count_similarID():
#     count = 0
#     # for x in my_collection.find({}, {"_id": 1, "similarID": 1}):
#     for x in my_collection.find({"similarID": {"$ne": None}}, {"_id": 1, "similarID": 1, "文本内容": 1}):
#         x.get('similarID')
#         # print(x)
#         count = count + 1
#     return count
#     # print(count)

# def find_one_similarID():
#     x = my_collection.find_one({"similarID": {"$ne": None}}, {"_id": 1, "similarID": 1, "文本内容": 1})
#     print(x)
#     data = x.get('similarID')
#     # print(data)
#     return data

def find_similarID():
    i = my_collection.count_documents({"similarID": {"$ne": None}})
    for i, x in enumerate(my_collection.find({"similarID": {"$ne": None}}, {"_id": 1, "similarID": 1, "文本内容": 1})):
        data = x.get('similarID')
        print("-" * 10, i, "-" * 10, data)
        print(x.get("文本内容"))
        print()
        # data = ObjectId("5a3ccdc7ee6a8e14bc7c176d")
        print(find_wenben(data).get("文本内容"))
        print()


def find_wenben(id):
    for db1 in mongo_client.list_database_names():
        if db1 == "local":
            continue
        for collection1 in mongo_client[db1].list_collection_names():
            # print(db1, collection1)
            data1 = mongo_client[db1][collection1].find_one({"_id": id})
            if data1:
                return data1


if __name__ == '__main__':
    # i = 1
    # for i in range(count_similarID()):
        # print(find_wenben(find_one_similarID()))
    import time
    t1 = time.time()
    print(find_similarID())
    t2 = time.time()
    print("cost:", t2-t1)
