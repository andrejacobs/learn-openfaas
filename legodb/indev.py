from legodb.handler import handle
import os
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

    os.environ['queue-name'] = 'johnny5'
    os.environ['redis-url'] = 'redis://192.168.64.4:9988/0'

    event = Event()
    context = Context()
    # response = handle(event, context)
    # print(f'{event.path}')
    # pprint(response)
    # print('')

    event.method = 'PUT'
    event.path = '/legosets-download-images'
    response = handle(event, context)
    print(f'{event.path}')
    pprint(response)
    print('')
