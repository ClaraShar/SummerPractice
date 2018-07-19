import copy
import time

from bson import ObjectId

from write_excel import write_excel


def 操作mongo():
    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["liulutest"]['test']
    # print(col.update({"发布网站":"2"}, {"$set":{"发布网站":666}}))
    # print(col.update({"发布网站": "2"}, {"发布网站": 666}))
    # dic = {"t":"ceshi"}
    # col.insert_one(dic)

    # col.update({}, {'$rename': {"file_urls": "附件URL"}}, multi=True)
    # col.update({"发布网站": "重大税收违法-湖北地税2"}, {'$set': {"发布网站": "重大税收违法-湖北地税-行政处罚"}}, multi=True)
    # col.update({}, {'$set': {"CleanUp": 0}}, multi=True)

    client.close()


def 打印cleanup文本内容_每个发布网站一个(col_name):
    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    db = client["诚信数据CleanUp"]
    col = db[col_name]
    sites = col.distinct("发布网站")
    for index, site in enumerate(sites):
        a = col.find_one({"发布网站": site})
        print("----- %s %s %s------" % (index, site, a["_id"]))
        print(a["文本内容"])


def 文件夹压缩之前_检查文件路径_每个发布网站2个(col_name):
    import os
    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    db = client["诚信数据CleanUp"]
    col = db[col_name]
    sites = col.distinct("发布网站")
    应该有的目录 = set()
    for index, site in enumerate(sites):

        aa = col.find({"发布网站": site})
        for a in aa[:2]:
            # print("----- %s %s %s------" % (index, site, a["_id"]))
            应该有的目录.add(a["源html文件"][0].split('\\')[1])
            应该有的path = '\\'.join(["V:\诚信数据初爬", a["源html文件"][0]])

            if os.path.exists(应该有的path):
                print(index, site, "存在：", 应该有的path)
            else:
                print(index, site, "不存在：", 应该有的path)
                print(a["_id"])

    path = "V:\诚信数据初爬\%s_诚信数据" % (col_name)
    已经有的目录 = set(os.listdir(path))
    # print("应该有的目录:",len(应该有的目录),应该有的目录)
    # print("已经有的目录:",len(已经有的目录), 已经有的目录)
    print("缺失的目录", 应该有的目录 - 已经有的目录)
    print("多余的目录", 已经有的目录 - 应该有的目录)

    client.close()


def 查看所有的地址():
    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    db = client["诚信数据CleanUp"]
    col = db["银监会"]
    aa = col.find()
    for a in aa:
        发布网站 = a["发布网站"].split("-")[-1]
        文件夹 = a["源html文件"][0].split('\\')[1]
        if 发布网站 != 文件夹:
            print(a["_id"], a["发布网站"], a["源html文件"])

    client.close()


def str2list(ss):
    ll = []
    for s in ss.split('\n'):
        s = s.strip()
        if s:
            ll.append(s)
    return ll


def 打印cleanup中指定文本内容(col_name="重大税收违法", site="", word="", follow_lines=0, ids=[], num=0):
    def print_a(site, i, a, word, not_has_word_count):
        print("---------%s %s:%s ---------" % (site, i, a["URL"]))
        if word:
            has_word = False
            print_follow_line = 0
            for line in a["文本内容"].split('\n'):
                if print_follow_line:
                    print(line)
                    print_follow_line -= 1

                if word in line:
                    print(line)
                    has_word = True
                    print_follow_line = follow_lines

            if not has_word:
                not_has_word_count += 1

        else:
            print(a["文本内容"])

        return not_has_word_count

    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["诚信数据CleanUp"][col_name]
    if not ids:
        if site:
            aa = col.find({"发布网站": site})
        else:
            aa = col.find()
        not_has_word_count = 0
        if num:
            for i, a in enumerate(aa[:num]):
                print_a(site, i, a, word, not_has_word_count)
        else:
            for i, a in enumerate(aa):
                print_a(site, i, a, word, not_has_word_count)
    else:
        not_has_word_count = 0
        for i, id in enumerate(ids):
            id = ObjectId(id)
            a = col.find_one({"_id": id})
            print_a(site, i, a, word, not_has_word_count)

    if site:
        all_count = col.count({"发布网站": site})
    else:
        all_count = col.count()

    if word:
        print("总数 %s 个，没有word个数 %s 个" % (all_count, not_has_word_count))
    else:
        print("*" * 10)
        print("总数 %s 个" % all_count)

    client.close()


def 打印cleanup中指定文本内容_2(col_name="重大税收违法", site="重大税收违法-安徽地税", key="", value=1, word="检查机关", follow_lines=0, ids=[]):
    def print_all_a_values(url, key):
        aa = col.find({"URL": url})
        print(("-- %s 个 --" % (col.count({"URL": url}))))
        for a in aa:
            print("--结果: %s: %s @@@\n" % (key, a[key]))

    def print_a(site, i, a, key, word, not_has_word_count):
        print("---------%s %s:%s ---------" % (site, i, a["URL"]))
        if word:

            has_word = False
            print_follow_line = 0
            if not a["文本内容"]:
                a["文本内容"] = ''
            for line in a["文本内容"].split('\n'):
                if print_follow_line:
                    print(line)
                    print_follow_line -= 1

                if isinstance(word, list):
                    for w in word:
                        if w in line:
                            print(line)
                            has_word = True
                            print_follow_line = follow_lines
                else:
                    if word in line:
                        print(line)
                        has_word = True
                        print_follow_line = follow_lines

            if not has_word:
                not_has_word_count += 1
        else:
            print(a["文本内容"])

        if key:
            # print_all_a_values(a["URL"],key)
            print("--结果: %s: %s @@@" % (key, a[key]))
        return not_has_word_count

    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["诚信数据CleanUp"][col_name]
    if not ids:
        aa = col.find({"发布网站": site})
        not_has_word_count = 0
        for i, a in enumerate(aa):
            print_a(site, i, a, key, word, not_has_word_count)
    else:
        not_has_word_count = 0

        if value == 0:
            aa = col.find({"发布网站": site, key: None})
            for i, a in enumerate(aa):
                print_a(site, i, a, key, word, not_has_word_count)

        else:
            count = col.count({"发布网站": site, key: {"$not": {"$eq": None}}})
            sep_count = int(count / 10) + 1
            aa = col.find({"发布网站": site, key: {"$not": {"$eq": None}}})
            for i, a in enumerate(aa):
                if i % sep_count == 0:
                    print_a(site, i, a, key, word, not_has_word_count)

    if word:
        print("总数 %s 个，没有word个数 %s 个" % (col.count({"发布网站": site}), not_has_word_count))
    else:
        print("*" * 10)
        print("总数 %s 个" % (col.count({"发布网站": site})))

    client.close()


def 打印cleanup中指定文本内容为None和不为None的10个(col_name="重大税收违法", site="重大税收违法-安徽地税", key="", word="组织机构代码", follow_lines=2):
    print()
    print("X" * 30)
    print(key, "所有为空的")
    print("X" * 30)
    打印cleanup中指定文本内容_2(col_name, site, key, 0, word, follow_lines, ids=1)
    print()
    print()
    print("Y" * 30)
    print(key, "随机10条有取值的")
    print("Y" * 30)
    打印cleanup中指定文本内容_2(col_name, site, key, 1, word, follow_lines, ids=1)


def 确认cleanup中唯一标识没有重复(col_name="重大税收违法", site="", key="URL", key2="处罚决定书文号"):
    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["诚信数据CleanUp"][col_name]
    if site:
        aa = col.find({"发布网站": site})
    else:
        aa = col.find()
    dic = {}
    chongfu_count = 0
    for a in aa:
        value = a[key]
        if value in dic:
            if key2 in a:
                biaoshi = str(a["行政相对人名称"]) + str(a[key2])
            else:
                biaoshi = str(a["行政相对人名称"])
            if biaoshi in dic[value]:
                print("重复", value, a["行政相对人名称"], dic[value])
                chongfu_count += 1
            else:
                dic[value] += [biaoshi]
        else:
            dic[value] = [a["行政相对人名称"]]

    if site:
        print("总数 %s条,其中重复 %s条" % (col.count({"发布网站": site}), chongfu_count))
    else:
        print("总数 %s条,其中重复 %s条" % (col.count(), chongfu_count))
    client.close()


def 确认cleanup中文件保存地址是否正确(col_name="重大税收违法", site="", prefix_path="V:\诚信数据初爬", replace_word=''):
    import os
    def is_exists(path):
        if os.path.exists(path):
            return
        else:
            pass

    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["诚信数据CleanUp"][col_name]
    if site:
        count = col.count({"发布网站": site})
    else:
        count = col.count()
    sep_count = int(count / 10) + 1  #
    if site:
        aa = col.find({"发布网站": site})
    else:
        aa = col.find()

    for index, a in enumerate(aa):
        if index % sep_count == 0:
            htmls = [os.path.sep.join([prefix_path] + path.split('\\')) for path in a["源html文件"]]
            # htmls = [prefix_path+"\\"+path for path in a["源html文件"]]
            for file in htmls:
                file = file.replace('_诚信数据', replace_word)
                # file = file.replace('_诚信数据',"(诚信数据)")
                # file = file.replace('_诚信数据',"_诚信数据1")
                if os.path.exists(file):
                    pass
                else:
                    print(a["_id"], "不存在", file)
    print("--源html文件 检查 over--")

    client.close()


def 确认cleanup中行政相对人名称是不是包含在标题中(col_name="重大税收违法", site="重大税收违法-安徽地税"):
    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["诚信数据CleanUp"][col_name]
    aa = col.find({"发布网站": site})
    for a in aa:
        if not a["行政相对人名称"] or not a["标题"]:
            if a["行政相对人名称"] == a["标题"]:
                pass
            else:
                print("---------%s :%s ---------" % (site, a["URL"]))
                print("标题:", a["标题"])
                print("行政相对人名称:", a["行政相对人名称"])
            continue

        if a["行政相对人名称"] in a["标题"]:
            pass
        else:
            print("---------%s :%s ---------" % (site, a["URL"]))
            print("标题:", a["标题"])
            print("行政相对人名称:", a["行政相对人名称"])
    print("---- 确认cleanup中行政相对人名称是不是包含在标题中 ----over")
    client.close()


def 打印出全部的取值N列(col_name, site, key, n):
    print("*" * 100)
    print(key, "打印出全部的取值N列")
    print("*" * 100)

    from pymongo import MongoClient
    client = MongoClient("192.168.0.90:27017")
    col = client["诚信数据CleanUp"][col_name]
    aa = col.find({"发布网站": site})
    values = set()
    for a in aa:
        v = str(a[key])
        values.add(v)

    for i, v in enumerate(values):
        if (i + 1) % n == 0:
            print(v)
        else:
            print(v, end="\t|@|\t")

        client.close()

def 验证可能为None的keys(col_name, site, keys):
        from pymongo import MongoClient
        client = MongoClient("192.168.0.90:27017")
        col = client["诚信数据CleanUp"][col_name]
        aa = col.find({"发布网站": site})

        value_dict = {}

        has_value_keys = set()
        for a in aa:
            new_keys = copy.copy(keys)
            for k in keys:
                if k in a and a[k]:  # 有值
                    has_value_keys.add(k)
                    if k in value_dict:
                        # value_dict[k].add(a[k])
                        if isinstance(a[k], list):
                            value_dict[k].add(','.join(a[k]))
                        else:
                            value_dict[k].add(a[k])
                    else:

                        if isinstance(a[k], list):
                            value_dict[k] = {','.join(a[k])}
                        else:
                            value_dict[k] = {a[k]}

        有值的set = has_value_keys
        无值的set = set(keys) - has_value_keys

        print("=" * 50)
        print("有值的set")
        print("=" * 50)
        for k in 有值的set:
            print(k, value_dict[k], sep=":")
            print()

        print("=" * 50)
        print("无值的set")
        print("=" * 50)
        print(无值的set)

        client.close()

def 验证不能有的keys(col_name, site, 不能有的keys):
        from pymongo import MongoClient
        client = MongoClient("192.168.0.90:27017")
        col = client["诚信数据CleanUp"][col_name]
        a = col.find_one({"发布网站": site})
        has_keys = set()
        for k in 不能有的keys:
            if k in a:
                has_keys.add(k)

        有值的set = has_keys
        无值的set = set(不能有的keys) - has_keys

        print("=" * 50)
        print("不应该有的key,但有值")
        print("=" * 50)
        print(有值的set)

        print("=" * 50)
        print("不应该有的key,确实无值")
        print("=" * 50)
        print(无值的set)

        client.close()

def 重大税收违法测试工具():
        col_name = "重大税收违法"

        site = "重大税收违法-国税总局"

        type = 2

        default_follow_lines = 0

        if type == 1:
            #
            确认cleanup中唯一标识没有重复(col_name=col_name, site=site, key="URL")
            确认cleanup中文件保存地址是否正确(col_name=col_name, site=site, prefix_path="V:\诚信数据初爬", replace_word="(诚信数据)")
            打印cleanup中指定文本内容(col_name=col_name, site=site)
            确认cleanup中行政相对人名称是不是包含在标题中(col_name=col_name, site=site)
        elif type == 0:
            # 打印cleanup中指定文本内容(col_name=col_name, site=site,num=1)
            确认cleanup中文件保存地址是否正确(col_name=col_name, site=site, prefix_path="V:\诚信数据初爬", replace_word="_诚信数据_pushed")
            # 确认cleanup中文件保存地址是否正确(col_name=col_name, site=site, prefix_path="V:\诚信数据初爬", replace_word="_诚信数据1")
        else:
            write_excel("诚信数据CleanUp").run(col_name, site=site)

            可能为None的keys = [
                "发布时间",
                "行政相对人代码_1统一社会信用代码", "行政相对人代码_3工商登记码", "其他证件号码",

                "网页类型", "图片URL", "附件URL", "附件名称",
            ]
            不能有的keys = ["处罚决定书文号", "处罚机关", "案件名称",
                        "处罚生效日期", "数据更新时间", "处罚截止日期", ]

            key_word_tuple = [
                # ["发布时间",["录入时间"],default_follow_lines,[0,1]],
                # ["处罚机关",["单位"],default_follow_lines,[0,1]],
                ["行政相对人名称", ["纳税人名称"], default_follow_lines, [0, 1]],  # 0
                ["行政相对人代码_2组织机构代码", ["组织"], default_follow_lines, [0, 1]],
                ["行政相对人代码_4税务登记号", ["纳税人识别号"], default_follow_lines, [0, 1]],  # 2
                ["行政相对人代码_5居民身份证号", ["法定代表人"], default_follow_lines, [0, 1]],
                ["法定代表人或负责人姓别", ["法定代表人"], default_follow_lines, [0, 1]],  # 4
                ["法定代表人或负责人姓名", ["法定代表人"], default_follow_lines, [0, 1]],
                ["主要违法事实", ["主要违法事实"], default_follow_lines + 4, [1]],  # 6
                ["相关法律依据及处罚情况", ["相关法律"], default_follow_lines + 4, [1]],
                ["案件性质", ["案件性质"], default_follow_lines, [0, 1]],  # 8
                # ["案件性质", ["案件类型"], default_follow_lines, [0, 1]],
                ["负有直接责任的中介机构信息及其从业人员信息", ["中介"], default_follow_lines, [0, 1]],
                ["负有直接责任的财务负责人姓别", ["财务"], default_follow_lines, [0, 1]],  # 10
                ["负有直接责任的财务负责人姓名", ["财务"], default_follow_lines, [0, 1]],
                ["负有直接责任的财务负责人身份证号码或其他证件号码", ["财务"], default_follow_lines, [0, 1]],  # 12
            ]
            for info in key_word_tuple[6:]:
                key, word, follow_lines, methods = info[0], info[1], info[2], info[3]

                if 0 in methods:
                    打印出全部的取值N列(col_name, site, key, 2)
                    print()
                if 1 in methods:
                    打印cleanup中指定文本内容为None和不为None的10个(col_name=col_name, site=site, key=key, word=word,
                                                     follow_lines=follow_lines)
                    print()
            #
            验证可能为None的keys(col_name, site, 可能为None的keys)
            print()
            验证不能有的keys(col_name, site, 不能有的keys)

def 期货失信测试工具():
        col_name = "期货"

        default_follow_lines = 0
        确认cleanup中唯一标识没有重复(col_name=col_name, key="URL")
        # 确认cleanup中文件保存地址是否正确(col_name=col_name,  prefix_path="V:\诚信数据初爬", replace_word="(诚信数据)")
        # 打印cleanup中指定文本内容(col_name=col_name)

        # write_excel("诚信数据CleanUp").run(col_name)

        key_word_tuple = [
            # ["发布时间",["录入时间"],default_follow_lines,[0,1]],
            # ["处罚机关",["单位"],default_follow_lines,[0,1]],
            ["行政相对人名称", ["违法违规失信者姓名"], default_follow_lines, [0, 1]],  # 0
            ["行政相对人代码_2组织机构代码", ["组织"], default_follow_lines, [0, 1]],
            ["行政相对人代码_4税务登记号", ["税"], default_follow_lines, [0, 1]],  # 2
            ["行政相对人代码_5居民身份证号", ["法定代表人"], default_follow_lines, [0, 1]],
            ["法定代表人或负责人姓别", ["法定代表人"], default_follow_lines, [0, 1]],  # 4
            ["法定代表人或负责人姓名", ["法定代表人"], default_follow_lines, [0, 1]],
            ["主要违法事实", ["主要违法事实"], default_follow_lines + 4, [1]],  # 6
            ["相关法律依据及处罚情况", ["相关法律"], default_follow_lines + 4, [1]],
            ["案件性质", ["案件性质"], default_follow_lines, [0, 1]],  # 8
            # ["案件性质", ["案件类型"], default_follow_lines, [0, 1]],
            ["负有直接责任的中介机构信息及其从业人员信息", ["中介"], default_follow_lines, [0, 1]],
            ["负有直接责任的财务负责人姓别", ["财务"], default_follow_lines, [0, 1]],  # 10
            ["负有直接责任的财务负责人姓名", ["财务"], default_follow_lines, [0, 1]],
            ["负有直接责任的财务负责人身份证号码或其他证件号码", ["财务"], default_follow_lines, [0, 1]],  # 12
        ]
        # for info in key_word_tuple:
        #     key, word, follow_lines, methods = info[0], info[1], info[2], info[3]
        #
        #     if 0 in methods:
        #         打印出全部的取值N列(col_name, site, key, 2)
        #         print()
        #     if 1 in methods:
        #         打印cleanup中指定文本内容为None和不为None的10个(col_name=col_name, site=site, key=key, word=word,
        #                                          follow_lines=follow_lines)
        #         print()

def 测试工具():
        col_name = "食药监"
        # col_name = "安全黑名单"
        # col_name = "证监处罚"
        # col_name = "海关"
        # col_name = "行政处罚"
        # col_name = "期货2"
        # col_name = "环保处罚"

        # site = "行政处罚-吉林"
        site = "食药监-河北警示公告"

        write_excel("诚信数据CleanUp").run(col_name, site=site)
        # # # # #
        确认cleanup中唯一标识没有重复(col_name=col_name, site=site, key="URL")
        # # # #
        确认cleanup中文件保存地址是否正确(col_name=col_name, site=site, prefix_path="/home/liulu/nfs", replace_word="(诚信数据)")

        # 确认cleanup中行政相对人名称是不是包含在标题中(col_name=col_name, site=site)

        # 打印cleanup中指定文本内容(col_name=col_name, site=site)


        default_follow_lines = 0
        key_word_tuple = [
            # ["发布网站", [], default_follow_lines, [0]],  # 0
            # ["URL", [], default_follow_lines, [0]],
            # ["查询入口", [], default_follow_lines, [0]],#2
            # ["标题", ["案件名称","处罚名称"], default_follow_lines, [0,1]],
            # ["行政相对人名称", ["信用主体名称","行政相对人名称"], default_follow_lines, [0, 1]],  # 0
            # ["发布时间", ["数据更新"], default_follow_lines, [0, 1]],  # 0
            #
            # ["行政相对人代码_1统一社会信用代码", ["统一"], default_follow_lines, [0, 1]],
            # ["行政相对人代码_2组织机构代码", ["组织"], default_follow_lines, [0, 1]],
            # ["行政相对人代码_3工商登记码", ["工商"], default_follow_lines, [0, 1]],  # 2
            # ["行政相对人代码_4税务登记号", ["税务登记证号","税务登记号"], default_follow_lines, [0, 1]],  # 2
            # ["行政相对人代码_5居民身份证号", ["身份证"], default_follow_lines, [0, 1]],

            # ["处罚事由", ["处罚事由"], default_follow_lines, [1]],  # 6
            # ["处罚依据", ["处罚依据"], default_follow_lines, [1]],
            # ["处罚决定书文号", ["行政处罚决定书文号"], default_follow_lines, [1]],
            # ["处罚截止日期", ["处罚截止期"], default_follow_lines, [0, 1]],
            # ["处罚机关", ["处罚机关"], default_follow_lines, [0,1]],
            # ["处罚状态", ["处罚状态"], default_follow_lines, [0,1]],
            # ["处罚生效日期", ["处罚决定期"], default_follow_lines, [0, 1]],
            # ["处罚类别1", ["处罚类别1"], default_follow_lines, [0, 1]],
            # ["处罚类别2", ["处罚类别2"], default_follow_lines, [0, 1]],
            # ["处罚结果", ["处罚结果"], default_follow_lines, [0, 1]],
            # ["备注", ["备注"], default_follow_lines, [0, 1]],
            # ["数据更新时间", ["数据更新时间"], default_follow_lines, [0, 1]],
            # # ["数据来源部门", ["数据来源部门"], default_follow_lines, [0, 1]],
            # ["案件名称", ["案件名称"], default_follow_lines, [0, 1]],
            # ["法定代表人或负责人姓名", ["法人代表人姓名","法定代表人"], default_follow_lines , [0,1]],

            # ["处罚决定书文号", ["号"], default_follow_lines, [0, 1]],
            # ["文号", ["号"], default_follow_lines, [0, 1]],
            # ["处罚决定时间", ["日期","时间"], default_follow_lines , [1]],
            # ["处罚决定日期", ["日期"], default_follow_lines , [1]],
            # ["处罚机关", ["作出处罚决定海关"], default_follow_lines , [1]],
            # ["处罚类别1", ["处罚类别","处罚类型"], default_follow_lines , [1]],
            # ["救济渠道", ["救济渠道"], default_follow_lines , [1]],
            # ["案件名称", ["案件名称"], default_follow_lines, [0, 1]],
            # ["处罚结果", ["处罚决定"], default_follow_lines + 4, [1]],
            # ["案件性质", ["案件性质"], default_follow_lines, [0, 1]],  # 8
            # ["处罚结果", ["处罚决定"], default_follow_lines, [0, 1]],  # 8
            # # ["案件性质", ["案件类型"], default_follow_lines, [0, 1]],

            # ["负有直接责任的财务负责人姓别", ["财务"], default_follow_lines, [0, 1]],  # 10
            # ["负有直接责任的财务负责人姓名", ["财务"], default_follow_lines, [0, 1]],
            # ["负有直接责任的财务负责人身份证号码或其他证件号码", ["财务"], default_follow_lines, [0, 1]],  # 12

            # ["被处罚当事人_个人姓名", ["个人"], default_follow_lines+2, [0, 1]],  # 12
            # ["被处罚当事人_单位名称", ["单位"], default_follow_lines , [0, 1]],  # 12

        ]
        for info in key_word_tuple:
            key, word, follow_lines, methods = info[0], info[1], info[2], info[3]

            if 0 in methods:
                打印出全部的取值N列(col_name, site, key, 2)
                print()
            if 1 in methods:
                打印cleanup中指定文本内容为None和不为None的10个(col_name=col_name, site=site, key=key, word=word,
                                                 follow_lines=follow_lines)
                print()

if __name__ == '__main__':
        t1 = time.time()

        site = "食药监-黑龙江行政处罚"

        '''if "行政" in site or "违法" in site:
            col_name = site.split("-")[0] + "-行政处罚"
        if "闲置土地" in site:
            col_name = site.split("-")[0] + "-闲置土地"
        if "土地抵押" in site or '福建土地' in site:
            col_name = site.split("-")[0] + "-土地抵押"
        if "矿产抵押" in site or "矿权抵押" in site or '福建矿产' in site:
            col_name = site.split("-")[0] + "-矿权抵押"'''
        # 操作mongo()
        # 期货失信测试工具()
        # 重大税收违法测试工具()
        # 测试工具() #
        确认cleanup中唯一标识没有重复('食药监', site, key="URL")

        print(time.time() - t1)
