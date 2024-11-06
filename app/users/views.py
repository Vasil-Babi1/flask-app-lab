from flask import request, render_template, redirect, url_for, make_response, session, flash
from . import user_bp
from datetime import timedelta, datetime

@user_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        cookies = request.cookies
        color_scheme = session.get('color_scheme', 'light')
        return render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme)
    flash("Invalid: Session.", "danger")
    return redirect(url_for("users.login"))

@user_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('cookie-key-add')
    value = request.form.get('cookie-value-add')
    expire = int(request.form.get('cookie-expire-add', 0))
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(key, value, max_age=expire)
    flash('Success: cookie added.', 'success')
    return response

@user_bp.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    key = request.form.get('cookie-key-remove')
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(key, '', expires=0)
    flash('Success: cookie removed.', 'success')
    return response

@user_bp.route('/remove_all_cookies', methods=['POST'])
def remove_all_cookies():
    response = make_response(redirect(url_for('users.get_profile')))
    for key in request.cookies:
        response.set_cookie(key, '', expires=0)
    flash('Success: all cookies removed.', 'success')
    return response

@user_bp.route('/change_color_scheme')
def change_color_scheme():
    color_scheme = session.get('color_scheme', 'light')
    new_color_scheme = 'dark' if color_scheme == 'light' else 'light'
    session['color_scheme'] = new_color_scheme

    return redirect(url_for('users.get_profile'))

@user_bp.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username != "User" or password != "password":
            flash("Error: Invalid username or password.", "danger")
            return redirect(url_for("users.login"))
        session["username"] = username
        flash("Success: session added successfully.", "success")
        return redirect(url_for("users.get_profile"))
    return render_template("login.html")



@user_bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('users.get_profile'))

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



@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response
