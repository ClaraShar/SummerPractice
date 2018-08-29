import datetime


def add_tag():
    tag = []
    tag.append("标题")
    tag.append("网址")
    tag.append("发布日期")
    tag.append("文本内容")
    tag.append("下载日期")
    tag.append("分类")
    tag.append("来源网站")
    tag.append("金融分类")
    return tag


def add_script():
    script = []
    script.append("<br")
    script.append("function(")
    script.append("px;")
    script.append("innerHTML")
    script.append("document.")
    script.append("location.")
    script.append("href=")
    script.append("class=")
    script.append("width=")
    script.append("height=")
    script.append("<style")
    script.append("<h1")
    return script


def tagNULL(tag):
    if tag is None or tag == "":
        return True
    temp = tag.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
    if temp is None or tag == "":
        return True
    return False


def dateThanNow(date):
    now = datetime.datetime.now()
    if date > now:
        return True
    return False


def dateEquals1970(date):
    year = date.year
    if year == 1970:
        return True
    return False


def add_err_text():
    err_txt = {}
    err_txt["尾页"] = "关键字:尾页"
    err_txt["责编"] = "关键字:责编"
    err_txt["编者按"] = "关键字:编者按"
    err_txt["导读"] = "关键字:导读"
    err_txt["导语"] = "关键字:导语"
    err_txt["核心提示"] = "关键字:核心提示"
    err_txt["原文链接"] = "关键字:原文链接"
    err_txt["原标题"] = "关键字:原标题"
    err_txt["原题"] = "关键字:原题"
    err_txt["原文标题"] = "关键字:原文标题"
    err_txt["原题目"] = "关键字:原题目"
    err_txt["媒体来源"] = "关键字:媒体来源"
    err_txt["信息来源"] = "关键字:信息来源"
    err_txt["数据来源"] = "关键字:数据来源"
    err_txt["新闻来源"] = "关键字:新闻来源"
    err_txt["责任编辑"] = "关键字:责任编辑"
    err_txt["实习编辑"] = "关键字:实习编辑"
    err_txt["编辑"] = "关键字:编辑"
    err_txt["免责声明"] = "关键字:免责声明"
    err_txt["免费声明"] = "关键字:免费声明"
    err_txt["作者为"] = "关键字:作者为"
    err_txt["作者系"] = "关键字:作者系"
    err_txt["转载"] = "关键字:转载"
    err_txt["转自"] = "关键字:转自"
    err_txt["摘要"] = "关键字:摘要"
    err_txt["阅读原文"] = "关键字:阅读原文"
    err_txt["相关链接"] = "关键字:相关链接"
    err_txt["微信公众号"] = "关键字:微信公众号"
    err_txt["摘 要"] = "关键字:摘 要"
    err_txt["文／"] = "关键字:文／"
    err_txt["更多相关资讯"] = "关键字:更多相关资讯"
    err_txt["页："] = "关键字:页："
    err_txt["文/"] = "关键字: 文/"
    err_txt["二维码下载"] = "关键字: 二维码下载"
    err_txt["侵权请联系"] = "关键字: 侵权请联系"
    err_txt["声明："] = "声明："
    err_txt["来源："] = "来源："
    err_txt["上一页"] = "上一页"
    err_txt["下一页"] = "下一页"
    err_txt["導讀"] = "導讀"
    err_txt["導語"] = "導語"
    err_txt["原文鏈接"] = "原文鏈接"
    err_txt["原標題"] = "原標題"
    err_txt["原題"] = "原題"
    err_txt["原文標題"] = "原文標題"
    err_txt["原題目"] = "原題目"
    err_txt["媒體來源"] = "媒體來源"
    err_txt["信息來源"] = "信息來源"
    err_txt["數據來源"] = "數據來源"
    err_txt["新聞來源"] = "新聞來源"
    err_txt["責任編輯"] = "責任編輯"
    err_txt["編輯"] = "編輯"
    err_txt["免責聲明"] = "免責聲明"
    err_txt["免費聲明"] = "免費聲明"
    err_txt["作者為"] = "作者為"
    err_txt["轉載"] = "轉載"
    err_txt["轉自"] = "轉自"
    err_txt["閱讀原文"] = "閱讀原文"
    err_txt["相關鏈接"] = "相關鏈接"
    err_txt["微信公眾號"] = "微信公眾號"
    err_txt["更多相關資訊"] = "更多相關資訊"
    err_txt["頁："] = "頁："
    err_txt["二維碼下載"] = "二維碼下載"
    err_txt["侵權請聯系"] = "侵權請聯系"
    err_txt["聲明："] = "聲明："
    err_txt["來源："] = "來源："
    err_txt["上壹頁"] = "上壹頁"
    return err_txt
