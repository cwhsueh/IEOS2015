#!/usr/bin/env python

# python native module ---------------------------
import json
import argparse
import os.path
# tornado module ---------------------------------
import tornado.httpserver
import tornado.web
import tornado.ioloop
from tornado.options import define, options

# Custom module ----------------------------------
import subprocess
import time, RPi.GPIO as GPIO
import pygame

# Initialize stuff -------------------------------

cur_state   = { 'tv': False, 'light': False, 'stereo': False, 'fan': False }
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)


def main():
    parser = argparse.ArgumentParser(description='Raspberry Pi Server Server')
    parser.add_argument('port', type=int, help='Listening port for Raspberry Pi Server')
    args = parser.parse_args()
    print "Raspberry Pi Server is starting on", args.port, '......\n'

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

        device      = command['device_name']
        action      = command['action']
        number      = command['number']
        
        print 'Caught command...'
        # TV 
        if device == 'tv':
            if action == 'turn on':
                print '... Television ON'
                if cur_state['tv'] != True:
                    ret = subprocess.call(["irsend", "SEND_ONCE", "/home/pi/lircd.conf", "KEY_POWER"])
                    if ret == 0:
                        print 'Success!!'
                    else:
                        print 'Failed'
                    cur_state['tv'] = True
                else:
                    print 'Television is already ON.'

            elif action == 'turn off':
                print '... Television OFF'
                if cur_state['tv'] != False:
                    ret = subprocess.call(["irsend", "SEND_ONCE", "/home/pi/lircd.conf", "KEY_POWER"])
                    if ret == 0:
                        print 'Success!!'
                    else:
                        print 'Failed'
                    cur_state['tv'] = False
                else:
                    print 'Television is already OFF.'
            print '\n'


        # LIGHT 
        elif device == 'light':
            if action == 'turn on':
                print '... Light ON'
                if cur_state['light'] != True:
                    ret =  GPIO.output(4, 1)
                    if ret == None:
                        print 'Success!!'
                    else:
                        print 'Failed' 
                    cur_state['light'] = True
                else:
                    print 'Light is already ON.'

            else:
                print '... Light OFF'
                if cur_state['light'] != False:
                    ret =  GPIO.output(4, 0)
                    if ret == None:
                        print 'Success!!'
                    else:
                        print 'Failed' 
                    cur_state['light'] = False
                else:
                    print 'Light is already OFF.'
            print '\n'

        # STEREO
        elif device == 'stereo':
            if action == 'turn on':
                print '... Stereo ON'
                if cur_state['stereo'] == False:
                    pygame.mixer.init()
                    cur_state['stereo'] = True
                    pygame.mixer.music.set_volume(1)
                else:
                    print 'Stereo is already ON'

            elif action == 'change channel':
                if cur_state['stereo'] == True:
                    if number == 1:
                        print '... Stereo plays song #1'
                        pygame.mixer.music.load("/home/pi/Music/5566.mp3")
                        pygame.mixer.music.play()
                    elif number == 2:
                        print '... Stereo plays song #2'
                        pygame.mixer.music.load("/home/pi/Music/year.mp3")
                        pygame.mixer.music.play()
                    elif number == 3:
                        print '... Stereo plays song #3'
                        pygame.mixer.music.load("/home/pi/Music/when_dream_end.mp3")
                        pygame.mixer.music.play()
                else:
                    print 'Stereo is OFF now'

            elif action == 'volume up':
                print '... Stereo VOLUME UP'
                if cur_state['stereo'] == True:
                    if pygame.mixer.music.get_volume() != 1:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.5) 
                    else:
                        print 'Volume is at maximum.'
                else:
                    print 'Stereo is OFF now.'

            elif action == 'volume down':
                print '... Stereo VOLUME DOWN'
                if cur_state['stereo'] == True:
                    if pygame.mixer.music.get_volume() != 0:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.5) 
                    else:
                        print 'Volume is at minimum.'
                else:
                    print 'Stereo is OFF now.'

            elif action == 'turn off':
                print '... Stereo OFF'
                if cur_state['stereo'] == True:
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    cur_state['stereo'] = False 
                else:
                    print 'Stereo is already OFF'
            print '\n'



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
