# python native module ---------------------------
import json
import pprint
import argparse
import os.path
# tornado module ---------------------------------
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado.options import define, options

# Custom module ----------------------------------

# ------------------------------------------------

pp = pprint.PrettyPrinter(indent=4)


def main():
    parser = argparse.ArgumentParser(description='Raspberry Pi Server Server')
    parser.add_argument('port', type=int, help='Listening port for Raspberry Pi Server')
    args = parser.parse_args()
    print "Raspberry Pi Server is starting on", args.port, '......'

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(args.port)

    tornado.ioloop.IOLoop.instance().start()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', CommandHandler)]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)

class CommandHandler(tornado.web.RequestHandler):
    def post(self):
        command = json.loads(self.request.body)
        print 'POST recive:',
        pp.pprint(command)


        # Then u can do something with Command
        # comand = {
        #	 'device_name' : device_name,
        #	 'action'      : action,
        # 	 'number'      : number
        # }
        # .....
        # .....

if __name__ == '__main__':
    main()