from app import db

class ServiceDetails(db.Document):
    id = db.IntField()              # 参数id

    name = db.StringField()            # 参数名称

    api_address = db.StringField()            # 参数类型

    api_call_way = db.StringField()
    api_introduction = db.StringField()

    arguments = db.StringField()
    result_arguments = db.StringField()
    error_code = db.StringField()
    result = db.StringField()
    return_style = db.StringField()
    call_example = db.StringField()
    create_time = db.StringField()
    update_time = db.StringField()
    def __str__(self):
        return "service:{} - url:{}".format(self.name, self.description)
