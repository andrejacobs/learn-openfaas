import json

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


def get_list_of_legosets():
    set1 = {'LegoID': 21322,
        'Description': 'Pirates of Barracuda Bay', 
        'ProductURL':'',
        'ImageURL': ''
        }
    return {"sets": [set1]}
    

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
