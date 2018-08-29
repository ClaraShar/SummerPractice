class ErrType:
    def __init__(self, errtitle, explanation):
        self.errtitle = errtitle
        self.explanation = explanation

    def tostring(self):
        return "ErrType{" + "错误地址='" + self.errtitle + '\'' + "  错误详情='" + self.explanation + '\'' + '}'
