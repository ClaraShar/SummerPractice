import os

import xlwt
from pymongo import MongoClient


class write_excel:
    def __init__(self,db_name = "行政处罚(诚信数据)"):

        self.m = MongoClient("192.168.0.90:27017")
        # self.m = MongoClient("192.168.0.140:22222")
        self.db_name = db_name

    def run(self,col_name = None,site=''):

        workbook = xlwt.Workbook(encoding='gb2312')
        def write_table(workbook, table_name, fieldnames, aa,table_index):
            n = 0
            table_num = 0
            for a in aa:
                if n % 10 == 0:
                    print("写表",table_index,table_name, n)

                if n % 65536 == 0:
                    table_num += 1
                    # 创建一个新表,并写首行
                    if table_num == 1:
                        worksheet = workbook.add_sheet("%s."%(table_index)+table_name)
                    else:
                        worksheet = workbook.add_sheet("%s."%(table_index)+table_name + str(table_num))

                    for index, fieldname in enumerate(fieldnames):
                        worksheet.write(0, index, label=fieldname)
                    n += 1

                for index, fieldname in enumerate(fieldnames):
                    if fieldname in a and a[fieldname]:
                        worksheet.write(n % 65536, index,
                                        label=a[fieldname].strip()[:32767] if isinstance(a[fieldname], str) else str(a[fieldname])[:32767])
                    else:
                        worksheet.write(n % 65536, index,
                                        label='None')

                n += 1

        if col_name:
            if isinstance(col_name,str):
                col_names = [col_name]
                if not site:
                    file_name = self.db_name+"_"+col_name+".xls"
                    # file_name = os.path.join('/home/liulu/nfs/刘璐临时转移',self.db_name + "_" + col_name + ".xls")
                else:
                    file_name = self.db_name + "_" + col_name + "_" + site + ".xls"
                    # file_name =  os.path.join('/home/liulu/nfs/刘璐临时转移',self.db_name + "_" + col_name + "_" + site + ".xls")

            elif isinstance(col_name,list):
                col_names = col_name
                file_name = self.db_name + ".xls"
        else:
            col_names = self.m[self.db_name].collection_names()
            file_name = self.db_name + ".xls"

        for index,col_name in enumerate(col_names):
            col = self.m[self.db_name][col_name]
            # fieldnames = self.get_all_key(col_name)
            fieldnames = self.get_one_item_key(col_name)
            # fieldnames = self.必须的key()

            if not site:
                aa = col.find()
            else:
                # aa = col.find({"发布网站":site}).sort("发布时间",-1)
                aa = col.find({"发布网站": site})
            write_table(workbook, col_name, fieldnames, aa,index+1)

        workbook.save(file_name)
        self.m.close()

    def get_all_key(self,col_name):
        print("遍历collection:",col_name,"获取最大的keys集合，它可能需要一点时间...")
        col = self.m[self.db_name][col_name]
        aa = col.find()
        keys =set()
        for a in aa:
            keys = keys | set(a.keys())

        keys = list(keys)
        keys.sort()
        return keys

    def get_one_item_key(self,col_name):
        print("默认结构统一，只取一个例子得到keys。collection:", col_name)
        col = self.m[self.db_name][col_name]
        a = col.find_one()
        keys = set(list(a.keys()))
        keys_1 = ["发布网站","_id","URL","查询入口",
                  "标题","行政相对人名称", "文本内容", "发布时间",

                  "行政相对人代码_1统一社会信用代码","行政相对人代码_2组织机构代码","行政相对人代码_3工商登记码","行政相对人代码_4税务登记号","行政相对人代码_5居民身份证号"]
        keys_2 = ["网页类型",'图片URL','附件URL','附件名称',"文件保存地址","源html文件","下载时间"]

        keys_center = list(keys - set(keys_1) -set(keys_2))
        keys_center.sort()

        sort_keys = keys_1+keys_center+keys_2
        return sort_keys

    def 必须的key(self):
        need_keys = ["标题", "文本内容", "发布时间",
                     "行政相对人名称", "行政相对人代码_1统一社会信用代码", "行政相对人代码_2组织机构代码", "行政相对人代码_3工商登记码", "行政相对人代码_4税务登记号",
                     "行政相对人代码_5居民身份证号",
                     "网页类型", "发布网站", "URL", "下载时间", "文件保存地址",
                     "查询入口"]
        return need_keys


if __name__ == '__main__':
    import time
    t1 = time.time()

    ######## type1: write_excel 一系列的collections #########
    # sites_string = '''湖南
    # 兵团
    # '''
    # sites = []
    # for s in sites_string.split("\n"):
    #     s = s.strip()
    #     if s:
    #         sites.append(s)
    # write_excel("黑名单(诚信数据)").run(sites)

    ######## type2: write_excel 单个collection #########
    # write_excel("重大税收违法(诚信数据)").run("西藏国税")

    ######## type3: write_excel 单个collection 单个发布网站 #########
    site = "食药监-黑龙江行政处罚"

    '''if "行政" in site or "违法" in site:
        col_name = site.split("-")[0] + "-行政处罚"
    if "闲置土地" in site:
        col_name = site.split("-")[0] + "-闲置土地"
    if "土地抵押" in site or '福建土地' in site:
        col_name = site.split("-")[0] + "-土地抵押"
    if "矿产抵押" in site or "矿权抵押" in site or '福建矿产' in site:
        col_name = site.split("-")[0] + "-矿权抵押"'''

    write_excel("诚信数据CleanUp").run("食药监",site)



    print("cosst:",time.time()-t1)