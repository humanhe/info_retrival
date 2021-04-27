from flask import Flask, render_template, request, redirect, url_for, session
from elasticsearch import Elasticsearch
from search import get_search_result
from home_page_results_display import front_page
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'key'


@app.route('/')
def home_page():
    obj = front_page()
    home_data = obj.get_home_page_display_data()

    return render_template('insert_query.html', home_data = home_data)


@app.route('/', methods=['POST'])
def submit_a_query():
    text = request.form["query"]
    # processed_texgt = text.upper()
    session['a_query'] = text

    return redirect(url_for('display_recipe'))


@app.route("/recipe_result")
def display_recipe():
    user_query = session.get('a_query')
    obj = get_search_result()
    data, updated_query = obj.search(user_query)
    # dict_temp = {}
    # dict_temp[869] = '869-Simple-Guacamole-PIN-7-683x1024.png'
    # dict_temp[956] = '956-Simple-Guacamole-PIN-7-683x1024.png'
    # dict_temp[1482] = '1482-jessica-gavin-main.jpg'
    # list_temp = []
    # list_temp.append('869-Simple-Guacamole-PIN-7-683x1024.png')
    # list_temp.append('956-Simple-Guacamole-PIN-7-683x1024.png')
    # list_temp.append('1482-jessica-gavin-main.jpg')
    # data[0].append('869-Simple-Guacamole-PIN-7-683x1024.png')
    # data[1].append('956-Simple-Guacamole-PIN-7-683x1024.png')
    # data[2].append('1482-jessica-gavin-main.jpg')
    table_header = ['Id', 'Web Page Title', 'Image', 'Short Description']
    return render_template("table.html", data = data, user_query = user_query, updated_query = updated_query, table_header = table_header)

# @app.route("/")
# def home_page():
#     today = datetime.today()
#     day_name = today.strftime("%A")
#     return render_template("insert_query.html", day=day_name)
#
# @app.route("/movies")
# def movies_page():
#     return render_template("table.html")


"""
Enable debugging and run in the terminal.
"""
if __name__ == '__main__':
    app.run(debug = True)
