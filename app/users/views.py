from flask import request, render_template, redirect, url_for, make_response
from . import user_bp
from datetime import timedelta, datetime

@user_bp.route("/hi/<string:name>") 
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("hi.html",
                            name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True) 
    print(to_url)
    return redirect(to_url)



@bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response