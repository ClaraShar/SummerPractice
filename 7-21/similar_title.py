# -*- coding:utf-8 -*-
import pymongo

mongo_client = pymongo.MongoClient('192.168.0.144', 22222)
db = mongo_client["21经济网(新闻)"]
my_collection = db["投资通-公告快递"]


def find_similar_title(title, id):
    for collection in db.list_collection_names():
        for x in db[collection].find({"标题": {"$eq": title}, "_id": {"$ne": id}}, {"标题": 1, "_id": 1}):
            if x:
                print(type(x))
                id1 = x.get("_id")
                print("相似数据id:", id1)
                data1 = x.get("标题")
                print("相似数据标题：", data1)
                return id1


def list_title():
    a = []
    for no, x in enumerate(my_collection.find({"标题": {"$ne": None}}, {"_id": 1, "similarID": 1, "标题": 1})):
        data = x.get('标题')
        print("第", no, "条标题：", data)
        i = x.get("_id")
        print("本条数据id:", i)
        d = x.get("similarID")
        print("本条数据相似数据id:", d)
        no1 = find_similar_title(data, i)
        if d == None and no1 != None:
            a.append(no)
        print()
    print("标题相同但未标记为相似ID的数据有：", len(a), "个，数据序号分别为：")
    print(a)


if __name__ == '__main__':
    list_title()
