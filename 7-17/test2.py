# -*- coding=utf-8 -*-
import csv    # 加载csv包便于读取csv文件

csv_file = open('demo.csv', encoding="utf-8")    # 打开csv文件
csv_reader_lines = csv.reader(csv_file)   # 逐行读取csv文件

data = []    # 创建列表准备接收csv各行数据

for one_line in csv_reader_lines:
    data.append(one_line)    # 将读取的csv分行数据按行存入列表‘data’中


def dedupe(items, key=None):
    seen = set()
    for item in items:
        # - 不可哈希值转可哈希值部分(核心)
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


result = list(dedupe(data, key=lambda x: tuple(x)))
out_file = open("out.csv", "w", newline='', encoding="utf-8")
out_csv_writer = csv.writer(out_file, dialect="excel")
out_csv_writer.writerow(result)
