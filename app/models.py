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

    def get_id_name(self):
        name_list = re.findall('<name>(.*?)</name>', self.cinfo)
        name = name_list[0] if name_list else ''
        return {'value': self.cid, 'label': name}

    @staticmethod
    def get_name(id):
        c = CustomerItem.query.filter_by(cid=id).first()
        return re.findall('<name>(.*?)</name>', c.cinfo)[0]


class ProductItem(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pinfo = db.Column(db.String(512))

    def __repr__(self):
        name_list = re.findall('<name>(.*?)</name>', self.pinfo)
        name = name_list[0] if name_list else ''
        return '<Product {}>'.format(name)

    def update_xml_id(self):
        pattern = '<product id="">'
        pattern_id = '<product id="' + str(self.pid) + '">'
        self.pinfo = self.pinfo.replace(pattern, pattern_id)

    def get_info(self):
        name_list = re.findall('<name>(.*?)</name>', self.pinfo)
        name = name_list[0] if name_list else ''
        count_list = re.findall('<num>(.*?)</num>', self.pinfo)
        count = count_list[0] if count_list else 0
        price_list = re.findall('<price>(.*?)</price>', self.pinfo)
        price = price_list[0] if price_list else 0
        return {'value': self.pid, 'label': name, 'count': count, 'price': price}

    @staticmethod
    def update(id, num):
        c = ProductItem.query.filter_by(pid=id).first()
        if not c:
            return
        old_num = re.findall('<num>(.*?)</num>', c.pinfo)[0]
        new_num = int(old_num) + int(num)
        c.pinfo = c.pinfo.replace('<num>' + old_num + '</num>', '<num>' + str(new_num) + '</num>')

    @staticmethod
    def get_name(id):
        c = ProductItem.query.filter_by(pid=id).first()
        return re.findall('<name>(.*?)</name>', c.pinfo)[0]


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(512))

    def __repr__(self):
        name_list = re.findall('<name>(.*?)</name>', self.cinfo)
        name = name_list[0] if name_list else ''
        return '<Trade {}>'.format(name)

    def update_xml(self):
        pattern = '<trade id="">'
        pattern_id = '<trade id="' + str(self.id) + '">'
        self.info = self.info.replace(pattern, pattern_id)
        pid = re.findall('<product>(.*?)</product>', self.info)[0]
        self.info = self.info.replace('<product>' + pid + '</product>',
                                      '<product>' + ProductItem.get_name(pid) + '</product>')
        cid = re.findall('<customer>(.*?)</customer>', self.info)[0]
        self.info = self.info.replace('<customer>' + cid + '</customer>',
                                      '<customer>' + CustomerItem.get_name(cid) + '</customer>')
        num = re.findall('<num>(.*?)</num>', self.info)[0]
        ProductItem.update(pid, -int(num))
