import pymongo

mongo_client = pymongo.MongoClient('192.168.0.34', 22222)
db = mongo_client["中国家电网(新闻)"]
# col = db["卫浴"]

for each_col in db.list_collection_names():
    if each_col != "system.indexes":
        db[each_col].update_many({}, {'$set': {'status': 0}})
