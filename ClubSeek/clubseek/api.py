from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json
from constants import *

apiEndpoints = Blueprint('apiEndpoints',__name__)

from main import connection

@apiEndpoints.route('/', methods=['GET'])
def get():
    return jsonify({ 'msg': 'Hello World'})

@apiEndpoints.route('/add_bar', methods=['POST'])
@expects_json(barSchema)
def add_bar():

    values = request.get_json()
    print(values)

    mycursor = connection.cursor()
    insert_stmt = (
    "INSERT INTO Bars (barName, wowFactor, capacity, currentTraffic) "
    "VALUES (%s, %s, %s, %s)"
    )
    data = (values["barName"], values["wowFactor"], values["capacity"], values["currentTraffic"])
    mycursor.execute(insert_stmt, data)
    mycursor.close()
    connection.commit()
    return values

@apiEndpoints.route('/del_bar', methods=['POST'])
@expects_json(barDeleteSchema)
def del_bar():

    values = request.get_json()
    print(values)

    mycursor = connection.cursor()
    del_stmt = "DELETE FROM Bars WHERE barName='%s'" % (values["barName"])
    mycursor.execute(del_stmt)
    mycursor.close()
    connection.commit()
    return values