from datetime import datetime
from random import randrange

from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
# from flask_sqlalchemy import SQLAlchemy

from dbConn import addUser

signupBlueprint = Blueprint('signup', __name__)
@signupBlueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pword']
        fname = request.form['fname']
        lname = request.form['lname']
        lat = randrange(505100, 553300, 1) / 1000
        long = randrange(1201000, 1204000, 1) / 1000
        if(addUser(fname, lname, username, password, lat, long)):
            return redirect("/login")
        else:
            error = 'That username already exists.'
            flash(error, category='error')
            # return render_template('signup.html', error=error, current_time=current_time)
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template('signup.html', error=error, current_time=current_time)
