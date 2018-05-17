import re
from app import db


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


db.Model.to_dict = to_dict


class CustomerItem(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    cinfo = db.Column(db.String(512))

    def __repr__(self):
        name_list = re.findall('<name>(.*?)</name>', self.cinfo)
        name = name_list[0] if name_list else ''
        return '<Customer {}>'.format(name)

    def update_xml_id(self):
        pattern = '<customer id="">'
        pattern_id = '<customer id="' + str(self.cid) + '">'
        self.cinfo = self.cinfo.replace(pattern, pattern_id)


class ProductItem(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pinfo = db.Column(db.String(512))

    def __repr__(self):
        name_list = re.findall('<name>(.*?)</name>', self.cinfo)
        name = name_list[0] if name_list else ''
        return '<Product {}>'.format(name)

    def update_xml_id(self):
        pattern = '<product id="">'
        pattern_id = '<product id="' + str(self.cid) + '">'
        self.cinfo.replace(pattern, pattern_id)


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(512))

    def __repr__(self):
        name_list = re.findall('<name>(.*?)</name>', self.cinfo)
        name = name_list[0] if name_list else ''
        return '<Trade {}>'.format(name)

    def update_xml_id(self):
        pattern = '<trade id="">'
        pattern_id = '<trade id="' + str(self.cid) + '">'
        self.cinfo.replace(pattern, pattern_id)
