import ErrType
import filter_text
import re
import datetime

class CheckDoc:
    def __init__(self, dbname, colname, doc):
        self.dbname = dbname
        self.colname = colname
        self.doc = doc

    def check_basic(self):
        list_errbasic = []
        keys = self.doc.keys()
        tag = filter_text.add_tag()
        for each_tag in tag:
            if each_tag not in keys:
                errtype = ErrType.ErrType("Document", "缺少" + each_tag)
                list_errbasic.append(errtype.tostring())
        return list_errbasic

    def check_title(self):
        list_errtitle = []
        title = self.doc.get("标题")
        if filter_text.tagNULL(title):
            errtype = ErrType.ErrType("标题", "标题为空")
            list_errtitle.append(errtype.tostring())
        script = filter_text.add_err_text()
        for each_script in script:
            if each_script in title:
                errtype = ErrType.ErrType("标题", "标题里面含有'" + each_script + "'")
                list_errtitle.append(errtype.tostring())
        return list_errtitle

    def check_url(self):
        list_errurl = []
        reg = "^(http|https|ftp)\\://([a-zA-Z0-9\\.\\-]+(\\:[a-zA-Z0-9\\.&%\\$\\-]+)*@)?((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9\\-]+\\.)*[a-zA-Z0-9\\-]+\\.[a-zA-Z]{2,4})(\\:[0-9]+)?(/[^/][a-zA-Z0-9\\.\\,\\?\\'\\\\/\\+&%\\$#\\=~_\\-@]*)*$"
        url = self.doc.get("网址")
        if filter_text.tagNULL(url):
            errtype = ErrType.ErrType("网址", "网址为空")
            list_errurl.append(errtype.tostring())
        if re.match(reg, url) is None:
            errtype = ErrType.ErrType("网址", "网址不是有效地址")
            list_errurl.append(errtype.tostring())
        return list_errurl

    def check_date(self):
        list_errdate = []
        fabu = self.doc.get("发布日期")
        if type(fabu) is not datetime.datetime:
            errtype = ErrType.ErrType("发布日期", "发布日期不是正确地址")
            list_errdate.append(errtype.tostring())
        else:
            if filter_text.dateThanNow(fabu):
                errtype = ErrType.ErrType("发布日期", "发布日期大于当前时间")
                list_errdate.append(errtype.tostring())
            elif filter_text.dateEquals1970(fabu):
                errtype = ErrType.ErrType("发布日期", "发布日期等于1970")
                list_errdate.append(errtype.tostring())

        xiazai = self.doc.get("下载日期")
        if type(xiazai) is not datetime.datetime:
            errtype = ErrType.ErrType("下载日期", "下载日期不是正确地址")
            list_errdate.append(errtype.tostring())
        else:
            if filter_text.dateThanNow(fabu):
                errtype = ErrType.ErrType("下载日期", "下载日期大于当前时间")
                list_errdate.append(errtype.tostring())

        return list_errdate

    def check_DownlodPath(self):
        list_errpath = []
        filepath = self.doc.get("文本存储路径")
        if filter_text.tagNULL(filepath):
            errtype = ErrType.ErrType("文本存储路径", "文本存储路径为空")
            list_errpath.append(errtype.tostring())
        return list_errpath

    def check_txt(self):
        list_errtxt =[]
        txt = self.doc.get("文本内容")
        if filter_text.tagNULL(txt):
            errtype = ErrType.ErrType("文本内容", "文本内容为空")
            list_errtxt.append(errtype.tostring())
        else:
            script = filter_text.add_script()
            for each_script in script:
                if each_script in txt:
                    errtype = ErrType.ErrType("文本内容", "脚本问题: 包含-> "+each_script)
                    list_errtxt.append(errtype.tostring())

        junks = filter_text.add_err_text()# 字典
        txtsub = re.split("\n", txt)# 字符串
        txtsub = "".join(txtsub)
        nice = set()

        if txtsub != "":
            for each_key, miaoshu in junks.items():
                if each_key in txtsub:
                    errtype = ErrType.ErrType(each_key, miaoshu)
                    temp = errtype.tostring()
                    if temp not in nice:
                        nice.add(temp)
                        list_errtxt.append(errtype.tostring())
        return list_errtxt

    def check_fenlei(self):
        list_errfenlei = []
        fenlei = self.doc.get("分类")
        sourceweb = self.doc.get("来源网站")
        jrfenlei = self.doc.get("金融分类")

        if filter_text.tagNULL(fenlei):
            errtype = ErrType.ErrType("分类", "分类为空")
            list_errfenlei.append(errtype.tostring())
        else:
            if fenlei != "新闻":
                errtype = ErrType.ErrType("分类", "分类不是新闻类型")
                list_errfenlei.append(errtype.tostring())

        if filter_text.tagNULL(sourceweb):
            errtype = ErrType.ErrType("来源网站", "来源网站为空")
            list_errfenlei.append(errtype.tostring())
        else:
            if sourceweb not in self.dbname:
                errtype = ErrType.ErrType("来源网站", "来源网站命名非正规命名")
                list_errfenlei.append(errtype.tostring())

        if filter_text.tagNULL(jrfenlei):
            errtype = ErrType.ErrType("金融分类", "金融分类为空")
            list_errfenlei.append(errtype.tostring())
        else:
            if jrfenlei not in self.colname:
                errtype = ErrType.ErrType("金融分类", "金融分类命名非正规命名")
                list_errfenlei.append(errtype.tostring())
        return list_errfenlei

    def check_ALL(self):
        list = self.check_basic()
        # list1 = self.check_title()
        list2 = self.check_url()
        list3 = self.check_date()
        # list4 = self.check_DownlodPath()
        list5 = self.check_txt()
        list6 = self.check_fenlei()
        # list.extend(list1)
        list.extend(list2)
        list.extend(list3)
        # list.extend(list4)
        list.extend(list5)
        list.extend(list6)

        return list
