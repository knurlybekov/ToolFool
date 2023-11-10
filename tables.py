import re
from datetime import datetime

import flask_login
import numpy as np
from flask import Blueprint, render_template, request, send_file
from flask_paginate import Pagination, get_page_args
import pandas as pd
from flask_login import login_required
from dbConn import connection, getOrders, getToolsA

tables_bp = Blueprint('tables', __name__)
# df = None

# 386ce9d230e54b3bb0f64db8b0da1238


@tables_bp.route('/tables', methods=['GET', 'POST'])
@login_required
def tables():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    menu_items = [
        {'value': 'Tools', 'label': 'Tools'},
        {'value': 'Orders', 'label': 'Orders'}
    ]
    # selected_menu_item = request.args.get('menu')
    # selected_wip_item = request.args.get('wip-items')
    # nameFind = request.args.get('nameFind')
    # startDate = request.args.get('startdate')
    # endDate = request.args.get('enddate')
    # getDF(selected_menu_item)
    page = request.args.get('page', 1, type=int)
    table_html, pagination = get_table(page=page)
    return render_template("tables.html", menu_items=menu_items, table_html=table_html, pagination=pagination, current_time=current_time)


def get_table(page=1, per_page=10):
    selected_menu_item = form_submit()
    df = getDF(selected_menu_item)
    print(df)
    pd.set_option('display.max_colwidth', None)  # display full column width
    pd.set_option('display.max_columns', None)  # display all columns
    pd.set_option('display.width', None)  # auto-detect terminal width
    df.index = np.arange(1, len(df) + 1)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 10
    offset = (page - 1) * per_page
    paginated_df = df.iloc[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=len(df), css_framework='bootstrap4')
    return paginated_df.to_html(classes='table table-hover table-bordered'), pagination


def getDF(selected_menu_item):
    if selected_menu_item == 'Tools':
        numbers = re.findall(r'\d+', str(flask_login.current_user))
        print(int(numbers[0]))
        return getToolsA(int(numbers[0]))
    elif selected_menu_item == 'Orders':
        numbers = re.findall(r'\d+', str(flask_login.current_user))
        print(int(numbers[0]))
        return getOrders(int(numbers[0]))
    else:
        return pd.DataFrame()


def form_submit():
    if request.method == 'POST':
        selected_menu_item = request.form.get('menu')

    elif request.method == 'GET':
        selected_menu_item = request.args.get('menu')

    else:
        selected_menu_item = None




# @tables_bp.route('/tables/download_csv',methods=['GET', 'POST'])
# def download_csv():
#     df = getemp()
#     csv_data = df.to_csv(index=False)
#     # convert dataframe to CSV and save to a temporary file
#     with open('emplogin.csv', 'w') as f:
#         f.write(csv_data)
#
#     # send the file to the client's web browser
#     return send_file('emplogin.csv', as_attachment=True)













# @tables.route('/tables', methods=['GET', 'POST'])
# @login_required
# def tables():
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     menu_items = [
#         {'value': 'Employees', 'label': 'Employees'},
#         {'value': 'Tools', 'label': 'Tools'},
#         {'value': 'Works in process', 'label': 'Works in process'}
#     ]
#     conn = connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT s_id, s_name FROM side')
#     wip_items = [{'value': None, 'label': 'All'}]
#     for row in cursor:
#         wip_items.append({'value': row[0], 'label': row[1]})
#     selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page = form_submit()
#     table_html, pagination = get_table(selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page)
#     return render_template("tables.html", menu_items=menu_items,wip_items=wip_items,table_html=table_html, pagination=pagination,current_time=current_time)
#
#
# def get_table(selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page):
#     df = getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate)
#     pd.set_option('display.max_colwidth', None)  # display full column width
#     pd.set_option('display.max_columns', None)  # display all columns
#     pd.set_option('display.width', None)  # auto-detect terminal width
#     df.index = range(1, len(df) + 1)
#     offset = (page - 1) * per_page
#     paginated_df = df.iloc[offset: offset + per_page]
#     pagination = Pagination(page=page, per_page=per_page, total=len(df), css_framework='bootstrap4')
#     return paginated_df.to_html(classes='table table-hover table-bordered'), pagination
#
#
# def getDF(selected_menu_item, selected_wip_item, nameFind, startDate, endDate):
#     if selected_menu_item == 'Employees':
#         return tableEmployees()
#     elif selected_menu_item == 'Tools':
#         return tableTools(selected_wip_item)
#     elif selected_menu_item == 'Works in process':
#         return tableWorkinprocess(selected_wip_item, startDate, endDate, nameFind)
#     else:
#         return pd.DataFrame()
#
#
# def form_submit():
#     selected_menu_item = request.args.get('menu', default=None, type=str)
#     selected_wip_item = request.args.get('wip-items', default=None, type=int)
#     nameFind = request.args.get('nameFind', default=None, type=str)
#     startDate = request.args.get('startdate', default=None, type=str)
#     endDate = request.args.get('enddate', default=None, type=str)
#     page = request.args.get('page', default=1, type=int)
#     per_page = request.args.get('per_page', default=10, type=int)
#     return selected_menu_item, selected_wip_item, nameFind, startDate, endDate, page, per_page

