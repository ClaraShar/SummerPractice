# -*-coding:utf-8-*-
# 导入必须的csv库
import csv
import codecs

# 创建临时文件temp.csv找出所需要的列
temp_file = open("temp.csv", "w", newline='', encoding='utf-8')  # 如果不指定newline='',则每写入一行将有一空行被写入
temp_csv_writer = csv.writer(temp_file, dialect="excel")

# 读取demo.csv文件，此时只有指定的一列数据
with open('demo.csv', encoding='utf-8') as file:
    temp_read_csv = csv.reader(file, delimiter=',')
    for row in temp_read_csv:  # 取出关联企业-排序_ORG3.csv所有列数据
        temp = [row[0]]  # 得到指定列数据
        temp_csv_writer.writerow(temp)
temp_file.close()

# -------------------------创建临时文件temp0-------------------------
# 创建临时文件temp0.csv找出所需要的列
temp0_file = open("temp0.csv", "w", newline='', encoding='utf-8')  # 如果不指定newline='',则每写入一行将有一空行被写入
temp0_csv_writer = csv.writer(temp0_file, dialect="excel")

# 读取demo.csv文件，此时只有指定的一列数据
with open('demo.csv', encoding='utf-8') as file:
    temp0_read_csv = csv.reader(file, delimiter=',')
    for row in temp0_read_csv:  # 取出关联企业-排序_ORG3.csv所有列数据
        temp0 = [row[0], row[1], row[2]]  # 得到指定列数据
        temp0_csv_writer.writerow(temp0)
temp0_file.close()
# --------------------------/////////////////-------------------------

# 在临时文件基础上匹配所要找的数据,计算出次数生成out.csv文件
out = []  # 新建数组来保存指定列的每行数据
out0 = []
out_time = []  # 新建数组来保存指定列的每行数据出现的次数
out_file = open("out.csv", "w", newline='', encoding="utf-8")
out_csv_writer = csv.writer(out_file, dialect="excel")
out_csv_writer.writerow(["ID", "TIMES"])  # 写入标题 数据，出现次数

# 读取temp.csv文件，此时只有指定的一列数据
# with open('temp.csv', encoding='UTF-8') as file2:
file2 = codecs.open('temp.csv', encoding='utf-8')
out_readcsv = csv.reader(file2, delimiter=',')
file3 = codecs.open('temp0.csv', encoding='utf-8')
out0_readcsv = csv.reader(file3, delimiter=',')

for St in out_readcsv:  # 循环取出列的每行数据
    out.append(St)  # append()将列的每行数据变为out链表(list)的后续增加的元素，即将列数据变为一维数组。
for Sr in out0_readcsv:  # 循环取出列的每行数据
    out0.append(Sr)  # append()将列的每行数据变为out0链表(list)的后续增加的元素，即将列数据变为一维数组。

for i in out:
    a = out.count(i)  # 取元素
    out_time.append(a)  # 得到出现的次数
    if a > 1:
        out.reverse()  # 将list反转来进行删除操作
        out0.reverse()
        for k in range(1, a):
            out.remove(i)  # 从后往前删除直到最前面的第一个为止，这样即删除了后面的，又保留了第一个！
            del out0[out.index(i)]
        out.reverse()  # 将list再反转回来,保证下次循环又是从原始顺序来删除
        out0.reverse()

    for j in range(len(out)):  # len()得到out1链表元素个数，依此作为time[]查找下标
        out_row = out0[j]
        out_csv_writer.writerow(out_row)
file2.close()
file3.close()
out_file.close()
