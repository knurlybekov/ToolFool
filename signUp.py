from datetime import datetime
from random import randint

from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
# from flask_sqlalchemy import SQLAlchemy

from dbConn import addUser

signUp = Blueprint('signIn', __name__)
@signUp.route('/SignUp', methods=['GET', 'POST'])
def signUp():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pword']
        fname = request.form['fname']
        lname = request.form['lname']
        lat = randint(553300, 505100)
        long = randint(1201000, 1204000)
        if(addUser(fname, lname, username, password, lat, long)):
            return render_template('login.html', error=error, current_time=current_time)
        else:
            error = 'That username already exists.'
            flash(error, category='error')
            return render_template('SignUp.html', error=error, current_time=current_time)
    messages = get_flashed_messages(with_categories=True)
    print(messages)