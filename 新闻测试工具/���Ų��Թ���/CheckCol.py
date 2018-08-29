import ErrType
import re

def check_col(db, colname):
    list_errcol = []
    count = db[colname].estimated_document_count()
    if count <=0:
        errtype = ErrType.ErrType(colname, "没有数据")
        list_errcol.append(errtype)
    if len(colname) >= 30:
        errtype = ErrType.ErrType(colname, "名称过长")
        list_errcol.append(errtype)
    if re.search(r'[._?]', colname):
        errtype = ErrType.ErrType(colname, "名称含有特殊符号")
        list_errcol.append(errtype)
    return list_errcol