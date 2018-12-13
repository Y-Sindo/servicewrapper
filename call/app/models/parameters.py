from app import db

class Parameters(db.Document):
    # 字段
    id = db.IntField()              # 参数id
    name = db.StringField()            # 参数名称
    description = db.StringField()     # 参数描述
    type = db.StringField()            # 参数类型
    example = db.StringField()         # 参数示例
    select = db.IntField()             # 参数是否在结果json中展示

    def __str__(self):
        return "service:{} - url:{}".format(self.name, self.description)
