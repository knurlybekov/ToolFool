from datetime import datetime
from random import randrange
import re

import flask_login
from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
# from flask_sqlalchemy import SQLAlchemy

from dbConn import addTool

toolprint = Blueprint('addtool', __name__)
@toolprint.route('/addtool', methods=['GET', 'POST'])
def addtool():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error = None
    if request.method == 'POST':
        toolname = request.form['toolName']
        desc = request.form['toolDescription']
        ui = re.findall(r'\d+', str(flask_login.current_user))
        ui = int(ui[0])
        price = request.form['price']
        if(addTool(toolname, desc, ui, price)):
            return redirect("/")
        else:
            error = 'Can not put tool in'
            flash(error, category='error')
            # return render_template('signup.html', error=error, current_time=current_time)
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template('addtool.html', error=error, current_time=current_time)