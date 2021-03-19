import os
import json
import mariadb

# GET /legosets : Returns the list of lego sets
# POST /legoset : Add a new lego set to the database

def handle(event, context):
    response = {'statusCode': 400}

    if event.method == 'GET':
        if event.path == '/legosets':
            legosets = get_list_of_legosets()
            response = {'statusCode': 200, 
                'body': legosets,
                'headers': {'Content-Type': 'application/json'}
                }
    elif event.method == 'POST':
        if event.path == '/legoset':
            response = add_new_legoset(event.body)
    
    return response


def load_secret(name):
    filepath = os.path.join('/var/openfaas/secrets/', name)
    with open(filepath) as f:
        secret = f.read()
    return secret


def database_connection():
    host = load_secret('database-host')
    user = load_secret('database-user')
    password = load_secret('database-password')
    database_name = os.environ.get('database-name')
    database_port = int(os.environ.get('database-port', '3306'))

    try:
        connection = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=database_port,
            database=database_name
        )
        return connection
    except mariadb.Error as error:
        print(f"Error: {error}")
        return None


def get_list_of_legosets():
    try:
        connection = database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT LegoID, Description FROM legosets")
        result = []
        for legoID, description in cursor:
            result.append({ "legoID": legoID, "description": description})
        return {"sets": result}
    except mariadb.Error as error:
        print(f"Error{error}")
        return {"error": f"{error}"}


def add_new_legoset(body):
    response = None
    try:
        inputJSON = json.loads(body.decode('utf8').replace("'", '"'))
        response = {
            'statusCode': 200,
            'body': {'received': inputJSON},
            'headers': {'Content-Type': 'application/json'}
        }
    except ValueError:
        response = {
            'statusCode': 400,
            'body': {'reason': 'Invalid JSON'},
            'headers': {'Content-Type': 'application/json'}
         }
    return response
