from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
import json

class CommandClient(object):

    def __init__(self):
        self.url = 'http://localhost:8888'

    def snedCommand(self, command):
        request = HTTPRequest(  
            self.url + '/',           # url to fetch
            'POST',                                                  # http method
            {'Content-type' : 'application/json'},                   # headers
            command,                                                    # body
        )
        
        def handle_response(response):
            if response.error:
                print('Error: ', response.error)
            else:
                print(response.body)
            IOLoop.instance().stop()

        self.fetch(request, handle_response)

    def fetch(self, request, callback):
        client =  AsyncHTTPClient()
        client.fetch(request, callback)
        IOLoop.instance().start()

def main():
    client = CommandClient()
    command = 'tv turn on'
    client.snedCommand(command)

if __name__ == '__main__':
    main()