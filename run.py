from app import app
from flask import render_template, request, redirect, session, url_for


@app.route('/', methods=['post', 'get'])
def index():
    return render_template('adminLogin.html')


@app.route('/adminLogin/', methods=['post', 'get'])
def admin_login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    if name != 'admin':
        msg = 'name error!'
    elif pwd != 'admin':
        msg = 'password error!'
    else:
        session['username'] = name
        return redirect(url_for('customer.get_customers'))

    return render_template('adminLogin.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
