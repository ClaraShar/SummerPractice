class Totxt:

    buffer = []

    '''生成指定格式的报告文件'''

    @staticmethod
    def put(url, miaoshu, oldText):
        text = "{\n\t\"detail\": \"" + miaoshu + "\",\n\t\"url\": \"" + url + "\",\n\t\"原文\": \"" + oldText + "\"\n" + "},"
        Totxt.buffer.append(text)

    '''根据网站名称生成一个包含网站错误的json文件'''
    @staticmethod
    def get_txt(dbname):
        text = "".join(Totxt.buffer)
        json = "[" + text[0: len(text) - 1] + "]"
        path = "D:\\Test\\" + dbname + ".txt"
        with open(path, 'w') as file:
            file.write(json)
