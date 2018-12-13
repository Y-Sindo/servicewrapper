from app import db

class Device(db.Document):
    # 字段
    devicename = db.StringField()
    macaddr = db.StringField()

    def __str__(self):
        return "devicename:{} - macaddr:{}".format(self.devicename, self.macaddr)

