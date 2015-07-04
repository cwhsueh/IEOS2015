# python native module --------------------------
import argparse
import os.path
import pprint
import json
# tornado module --------------------------------
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado.options import define, options
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
# pymongo module --------------------------------
from pymongo import MongoClient

# Custom module ---------------------------------
from CommandYacc import CommandParser

dburl = "mongodb://140.112.42.145:2016"
mongoserver = MongoClient(dburl)
db = mongoserver['ioes']
pp = pprint.PrettyPrinter(indent=4)

def main():
    parser = argparse.ArgumentParser(description='Command Server')
    parser.add_argument('port', type=int, help='Listening port for Command Server')
    args = parser.parse_args()

    print "Command Server is starting on", args.port, '......'
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(args.port)

    tornado.ioloop.IOLoop.instance().start()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', CommandHandler)]
        settings = dict(template_path=os.path.join(os.path.dirname(__file__), "templates"))
        super(Application, self).__init__(handlers, **settings)

class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        # get command string from 
        command = self.request.body
        print 'receive:', command
        
        # parsing command string, then get a dictionary
        try:
            command = CommandParser.parse(command.lower())
            print 'After parsing:',
            pp.pprint(command)
            
            # find device in database
            devices = db['devices']
            device  = devices.find_one({'device_name': command['device_name']})
            print 'in db:',
            pp.pprint(device)

            if device is not None:
                if command['action'] in device['actions']:
                    # request command to raspberry pi IP
                    # print 'send command to Raspberry Pi'
                    # request = CommandRequest('http://' + device['ip_address'])
                    # request.snedCommand(command)
                    
                    print 'Send command to Web page'
                    command['success'] = True
                    self.write(command)
                else:
                    # request "device cant do this action" to User Client
                    print 'device cant do this action'
                    self.write({
                        'success' : False,
                        'erorr':'device cant do this action'
                    })
                    # self.redirect('client IP')
            else:
                # request "no device" to User Client
                print 'no device'
                self.write({
                    'success' : False,
                    'error' : 'no device'
                })
        except:
            print 'Syntax Error'
            self.write({
                'success' : False,
                'error' : 'Syntax Error'
            })


class CommandRequest(object):

    def __init__(self, url):
        self.url = url

    def snedCommand(self, command):
        request = HTTPRequest(  
            self.url + '/',           # url to fetch
            'POST',                                                  # http method
            {'Content-type' : 'application/json'},                   # headers
            json.dumps( command, ensure_ascii=False, ).encode('utf8'),                                                   # body
        )
        
        def handle_response(response):
            if response.error:
                print('Error: ', response.error)
            else:
                print(response.body)

        self.fetch(request, handle_response)

    def fetch(self, request, callback):
        client = AsyncHTTPClient()
        client.fetch(request, callback)

if __name__ == '__main__':
    main()