""" Specifies routing for the application"""
from flask import render_template, request, jsonify, redirect
from app import app
from app import database as db_helper

@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_investment(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/edit/<int:investment_id>", methods=['POST'])
def update(investment_id):
    """ recieved post requests for entry updates """
    data = request.get_json()

    try:
        if "status" in data:
            print(0)
            db_helper.update_status_entry(investment_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            print(data["description"])
            db_helper.update_portfolio_name(investment_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            print(2)
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        print(3)
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/delete/<int:investment_id>", methods=['POST'])
def delete(investment_id):
    """ recieved post requests for entry delete """
    try:
        db_helper.delete_investment_by_ID(investment_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    print(result)
    return jsonify(result)

@app.route("/filter/<search>", methods=['GET'])
def filter(search):
    try:
        items = db_helper.filter_portfolios(search)
        result = {'success': True, 'response': 'Filtered results', 'link': '/search/'+search}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    print(result)
    return jsonify(result)

# @app.route("/search/<search>")
# def search(search):
#     """ returns rendered homepage """
#     items = db_helper.filter_portfolios(search)
#     return render_template("index.html", items=items)

@app.route("/search", methods=['POST'])
def search():
    projectpath = request.form['JohnJohnson']
    print(projectpath)
    try:
        items = db_helper.filter_portfolios(projectpath)
        result = {'success': True, 'response': 'Filtered results', 'link': '/search/'+search}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    print(result)
    return render_template("index.html", items=items)



@app.route("/")
def homepage():
    # return render_template("index.html")
    """ returns rendered homepage """
    items = db_helper.display_portfolio()
    return render_template("index.html", items=items)

@app.route("/query1")
def query1():
    # return render_template("index.html")
    """ returns rendered homepage """
    items = db_helper.advanced_query_one()
    return render_template("a1.html", items=items)
    

@app.route("/query2")
def query2():
    # return render_template("index.html")
    """ returns rendered homepage """
    items = db_helper.advanced_query_two()
    return render_template("a2.html", items=items)


@app.route("/storedtrue")
def storedtrue():
    # return render_template("index.html")
    """ returns rendered page after stored procedure """
    items = db_helper.stored_procedure(True)
    return render_template("stored_true.html", items=items)

@app.route("/storedfalse")
def storedfalse():
    # return render_template("index.html")
    """ returns rendered page after stored procedure """
    items = db_helper.stored_procedure(topStock=False)
    return render_template("stored_false.html", items=items)

@app.route("/trigger", methods=['POST'])
def trigger():
    # return render_template("index.html")
    """ returns rendered page after stored procedure """
    items = request.form['TriggerInput']
    items = items.split(':')
    db_helper.update_stock_api_ticker(items[0], items[1])
    return homepage()
