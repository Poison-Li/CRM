from app.customer import bp
from flask import request, render_template, jsonify, session, redirect, url_for
from app import db
from app.models import CustomerItem
import json


# con = mysql.connect()


@bp.route('/getCustomers/', methods=['post', 'get'])
def get_customers():
    if 'username' not in session:
        return redirect(url_for('index'))
    request.get_data()
    # cursor = con.cursor()
    # cursor.execute('select * from customerItem')
    # customer_tuple = cursor.fetchall()

    customer_tuple = CustomerItem.query.all()

    customers = [{'id': item.cid, 'info': item.cinfo} for item in customer_tuple]
    json1 = json.dumps({'customers': customers})

    return render_template('customers.html', customers=json1)


@bp.route('/addCustomer/', methods=['post', 'get'])
def add_customer():
    if 'username' not in session:
        return redirect(url_for('index'))
    receive = request.get_json()
    xml = receive['info']

    # cursor = con.cursor()  # ?get_db无效
    # cursor.execute('call addCustomer(%s)', xml)
    # cursor.execute('insert into customerItem (cinfo) VALUES (%s)', xml)
    # con.commit()
    # cursor.close()
    # con.close()

    customer = CustomerItem(cinfo=xml)
    db.session.add(customer)
    db.session.commit()
    customer.update_xml_id()
    db.session.commit()
    return jsonify({'msg': 'success', 'id': customer.cid})


@bp.route('/del/', methods=['post', 'get'])
def del_customer():
    if 'username' not in session:
        return redirect(url_for('index'))
    id = request.args.get('id')

    # cursor = con.cursor()
    # cursor.execute('delete from customerItem where cid=%s', id)
    # con.commit()
    # cursor.close()

    customer = CustomerItem.query.filter_by(cid=id).first_or_404()
    if customer:
        db.session.delete(customer)
        db.session.commit()

    return jsonify({'msg': 'success'})


@bp.route('/getModify', methods=['get', 'post'])
def get_modify():
    if 'username' not in session:
        return redirect(url_for('index'))
    id = request.args.get('id')
    return render_template('customer_modify.html', id=id)


@bp.route('/modify/', methods=['post', 'get'])
def modify_customer():
    if 'username' not in session:
        return redirect(url_for('index'))
    receive = request.get_json()
    id = receive['id']
    info = receive['info']

    # cursor = con.cursor()
    # cursor.execute('update customerItem set cinfo = %s where cid=%s', (info, int(id)))
    # con.commit()
    # cursor.close()

    customer = CustomerItem.query.filter_by(cid=id).first_or_404()
    if customer:
        customer.cinfo = info
        db.session.commit()

    return jsonify({'msg': 'success'})
