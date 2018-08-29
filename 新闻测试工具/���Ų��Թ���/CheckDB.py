import ErrType


def check_db(db, dbname):
    list_errdb = []
    if "(新闻)" not in dbname:
        errtype = ErrType.ErrType(db.name, "末尾 '(新闻)' 关键字")
        list_errdb.append(errtype)
    if len(dbname) > 30:
        errtype = ErrType.ErrType(db.name, "db名称太长")
        list_errdb.append(errtype)

    col = db.list_collection_names()
    if len(col) <= 0:
        errtype = ErrType.ErrType(db.name, "db没有数据")
        list_errdb.append(errtype)
    return list_errdb
