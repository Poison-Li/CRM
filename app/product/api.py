from app.product import bp
from flask import request, render_template, jsonify, session, redirect, url_for
from app import db
from app.models import ProductItem
import json


# con = mysql.connect()


@bp.route('/getProducts/', methods=['post', 'get'])
def get_products():
    if 'username' not in session:
        return redirect(url_for('index'))
    request.get_data()

    # cursor = con.cursor()
    # cursor.execute('select * from productItem')
    # product_tuple = cursor.fetchall()
    # cursor.close()

    product_tuple = ProductItem.query.all()

    products = [{'id': item.pid, 'info': item.pinfo} for item in  product_tuple]
    json1 = json.dumps({'products': products})

    return render_template('products.html', products=json1)


@bp.route('/addProduct/', methods=['post', 'get'])
def add_product():
    if 'username' not in session:
        return redirect(url_for('index'))
    receive = request.get_json()
    xml = receive['info']

    # cursor = con.cursor()  # ?get_db无效
    # cursor.execute('insert into productItem (pinfo) VALUES (%s)', xml)
    # con.commit()
    # cursor.close()
    # con.close()

    product = ProductItem(pinfo=xml)
    db.session.add(product)
    db.session.commit()
    product.update_xml_id()
    db.session.commit()

    return jsonify({'msg': 'success', 'id': product.pid})


@bp.route('/del/', methods=['post', 'get'])
def del_product():
    if 'username' not in session:
        return redirect(url_for('index'))
    id = request.args.get('id')

    # cursor = con.cursor()
    # cursor.execute('delete from productItem where pid=%s', id)
    # con.commit()
    # cursor.close()

    product = ProductItem.query.filter_by(pid=id).first_or_404()
    if product:
        db.session.delete(product)
        db.session.commit()

    return jsonify({'msg': 'success'})


@bp.route('/getModify', methods=['get', 'post'])
def get_modify():
    if 'username' not in session:
        return redirect(url_for('index'))
    id = request.args.get('id')
    return render_template('product_modify.html', id=id)


@bp.route('/modify/', methods=['post', 'get'])
def modify_product():
    if 'username' not in session:
        return redirect(url_for('index'))
    receive = request.get_json()
    id = receive['id']
    info = receive['info']

    # cursor = con.cursor()
    # cursor.execute('update productItem set pinfo = %s where pid=%s', (info, int(id)))
    # con.commit()
    # cursor.close()

    product = ProductItem.query.filter_by(pid=id).first_or_404()
    if product:
        product.pinfo = info
        db.session.commit()

    return jsonify({'msg': 'success'})
