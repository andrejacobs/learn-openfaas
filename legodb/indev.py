from legodb.handler import handle
from pprint import pprint

class Event:
    def __init__(self):
        self.body = None
        self.headers = None
        self.method = 'GET'
        self.query = None
        self.path = '/legosets'

class Context:
    def __init__(self):
        self.hostname = 'localhost'

if __name__ == "__main__":
    event = Event()
    context = Context()
    response = handle(event, context)
    pprint(response)
