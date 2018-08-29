import pymongo
import CheckDoc
import random
import Totxt
import traceback
import re
import ErrType

mongo_client = pymongo.MongoClient('192.168.0.90', 27017)
db = mongo_client["今晚网(新闻)"]


def check():
    dic1 ={}
    set1 = set()
    colnames = db.list_collection_names()
    for each_col in colnames:
        # if each_col != "system.indexes":
        for each_doc in db[each_col].find():
            url = each_doc.get("网址")
            example = CheckDoc.CheckDoc(db.name, each_col, each_doc)
            list1 = example.check_ALL()
            s = str(list1).replace("[", "").replace("]", "").replace("\"", "")

            if len(list1) > 0:
                if s in set1:
                    li3 = list(dic1.get(s))
                    li3.append(url)
                    dic1[s] = li3
                else:
                    set1.add(s)
                    li2 = []
                    li2.append(url)
                    dic1[s] = li2

    dic2 = {}
    for key in dic1:
        value = dic1[key] # value是错误类型的url
        o = random.choice(value) # 这个地方是优化的关键
        dic2[key] = o
    err_key_list = []
    for key in dic2:
        err_key_list.append(key)

    num = 0
    for s in err_key_list:
        print(s + " " + dic2[s])
        url = str(dic2[s])
        Totxt.Totxt.put(url, s, str(num))
        num += 1
    try:
        Totxt.Totxt.get_txt(db.name)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
    print(num)


def check_single(errtitle, explanation):
    list1 = []
    dic1 = {}
    li = []
    errtype = ErrType.ErrType(errtitle, explanation)
    temp = errtype.tostring()
    s = str(temp).replace("[", "").replace("]", "").replace("\"", "")
    colnames = db.list_collection_names()
    for each_col in colnames:
        for each_doc in db[each_col].find():
            url = each_doc.get("网址")
            txt = each_doc.get("文本内容")
            txtsub = re.split("\n", txt)  # 字符串
            txtsub = "".join(txtsub)
            if txtsub != "" and errtitle in txtsub:
                li.append(url)
                dic1[s] = li

    num = 0
    for each_url in dic1[s]:
        print(each_url)
        # print(s + " " + each_url)
        each_url = str(each_url)
        Totxt.Totxt.put(each_url, s, str(num))
        num += 1
    try:
        Totxt.Totxt.get_txt(db.name)
    except Exception as e:
        exstr = traceback.format_exc()
        print(exstr)
    print(num)


if __name__ == '__main__':
    check() #程序主入口
    # check_single("作者为", "作者为")# 这里给出错误类型
    # 后面还有，再说啦


