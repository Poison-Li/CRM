from app.trade import bp
import re
from flask import request, render_template, jsonify, session, redirect, url_for
from app import db
from app.models import CustomerItem, ProductItem, Trade
import json

# con = mysql.connect()
con = "ee"


@bp.route('/getTrades/', methods=['post', 'get'])
def get_trades():
    if 'username' not in session:
        return redirect(url_for('index'))
    request.get_data()

    # cursor = con.cursor()
    # cursor.execute('select * from trade')
    # trade_tuple = cursor.fetchall()
    # cursor.close()

    trade_tuple = Trade.query.all()

    trades = [{'id': item.id, 'info': item.info} for item in trade_tuple]
    json1 = json.dumps({'trades': trades})

    customers = [item.get_id_name() for item in CustomerItem.query.all()]

    products = [item.get_info() for item in ProductItem.query.all()]

    return render_template('trades.html', trades=json1, customers=customers, products=products)


@bp.route('/addTrade/', methods=['post', 'get'])
def add_trade():
    if 'username' not in session:
        return redirect(url_for('index'))
    receive = request.get_json()
    xml = receive['info']

    # cursor = con.cursor()  # ?get_db无效
    # cursor.execute('insert into trade (tradeinfo) VALUES (%s)', xml)
    # con.commit()
    # cursor.close()

    trade = Trade(info=xml)
    db.session.add(trade)
    db.session.commit()
    trade.update_xml()

    db.session.commit()

    return jsonify({'msg': 'success', 'id': trade.id})


@bp.route('/del/', methods=['post', 'get'])
def del_trade():
    if 'username' not in session:
        return redirect(url_for('index'))
    id = request.args.get('id')

    trade = Trade.query.filter_by(id=id).first_or_404()

    old_num = re.findall('<num>(.*?)</num>', trade.info)[0]

    pid = re.findall('<pid>(.*?)</pid>', trade.info)[0]

    ProductItem.update(pid, int(old_num))

    if trade:
        db.session.delete(trade)
        db.session.commit()

    return jsonify({'msg': 'success'})


@bp.route('/getModify', methods=['get', 'post'])
def get_modify():
    if 'username' not in session:
        return redirect(url_for('index'))
    id = request.args.get('id')
    return render_template('trade_modify.html', id=id)


@bp.route('/modify/', methods=['post', 'get'])
def modify_trade():
    if 'username' not in session:
        return redirect(url_for('index'))
    receive = request.get_json()
    id = receive['id']
    info = receive['info']

    # cursor = con.cursor()
    # cursor.execute('update trade set tradeinfo = %s where id=%s', (info, int(id)))
    # con.commit()
    # cursor.close()

    trade = Trade.query.filter_by(id=id).first_or_404()
    if trade:
        trade.info = info
        db.session.commit()

    return jsonify({'msg': 'success'})
