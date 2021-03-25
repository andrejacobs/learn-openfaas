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
    print(f'{event.path}')
    pprint(response)
    print('')

    event.method = 'PUT'
    event.path = '/legosets-download-images'
    response = handle(event, context)
    print(f'{event.path}')
    pprint(response)
    print('')

    # # Test the query for getting the next batch of images to download
    # print('Sets that need an image:')
    # from legodb.models import *
    # from legodb.utils import *
    # session = create_database_session()
    # needImages = get_legosets_that_need_an_image_download(session)
    # for legoset in needImages:
    #     pprint({
    #         'legoID': legoset.legoID,
    #         'description': legoset.description,
    #         'productURL': legoset.productURL,
    #         'imageURL': legoset.imageURL,
    #         'imagePath': legoset.imagePath
    #     })

    # session.close()