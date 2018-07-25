# -*- coding:utf-8 -*-
import pymongo
import xlwt

mongo_client = pymongo.MongoClient('192.168.0.144', 22222)
db = mongo_client["21经济网(新闻)"]
my_collection = db["快报"]


def auto_find_law(a):
    f = xlwt.Workbook("21经济网(新闻)-快报.xlsx")  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    sheet1.write(0, 0, "序号")
    sheet1.write(0, 1, "结果")
    sheet1.write(0, 2, "备注")
    for i in range(len(a)):
        sheet1.write(i+1, 0, a[i])
    # sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))
    f.save('21经济网(新闻)-快报.xls')  # 保存文件



def find_similar_title(title, id):
    for collection in db.list_collection_names():
        for x in db[collection].find({"标题": {"$eq": title}, "_id": {"$ne": id}}, {"标题": 1, "_id": 1, "文本内容": 1}):
            if x:
                id1 = x.get("_id")
                # print("相似数据id:", id1)
                data1 = x.get("标题")
                print("相似数据标题：", data1)
                txt1 = x.get("文本内容")
                print("相似数据文本内容：", txt1)
                return id1


def list_title():
    a = []
    for no, x in enumerate(my_collection.find({"标题": {"$ne": None}}, {"_id": 1, "similarID": 1, "标题": 1, "文本内容": 1})):
        data = x.get('标题')
        txt = x.get('文本内容')
        print("第", no, "条标题：", data)
        i = x.get("_id")
        # print("本条数据id:", i)0
        d = x.get("similarID")
        # print("本条数据相似数据id:", d)
        no1 = find_similar_title(data, i)
        if d == None and no1 != None:
            print("第", no, "条标题：", data)
            print('-' * 20)
            print("本条数据文本内容：", txt)
            a.append(no)
        print()
    print("标题相同但未标记为相似ID的数据有：", len(a), "个，数据序号分别为：")
    print(a)
    auto_find_law(a)


if __name__ == '__main__':
    list_title()
