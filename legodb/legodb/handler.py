import os
import json
from .models import LegoSet, database_session, get_all_legosets, create_legoset

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


def create_database_session():
    host = load_secret('database-host')
    user = load_secret('database-user')
    password = load_secret('database-password')
    schema = os.environ.get('database-name')
    port = int(os.environ.get('database-port', '3306'))

    session = database_session(host, port, user, password, schema)
    return session


def get_list_of_legosets():
    session = create_database_session()
    legosets = get_all_legosets(session)
    result = []

    for legoset in legosets:
        result.append({
            'legoID': legoset.legoID,
            'description': legoset.description,
            'productURL': legoset.productURL,
            'imageURL': legoset.imageURL
        })

    session.close()
    return {"sets": result}


def add_new_legoset(body):
    response = None
    try:
        inputJSON = json.loads(body.decode('utf8').replace("'", '"'))
        legoset = create_legoset(inputJSON)
        if legoset is None:
            raise ValueError()
        else:
            session = create_database_session()
            session.add(legoset)
            session.commit()
            session.refresh(legoset)
            newID = legoset.id
            session.close()

            response = {
                'statusCode': 200,
                'body': {'pkID': newID},
                'headers': {'Content-Type': 'application/json'}
        }
    except ValueError:
        response = {
            'statusCode': 400,
            'body': {'reason': 'Invalid JSON'},
            'headers': {'Content-Type': 'application/json'}
         }
    return response
