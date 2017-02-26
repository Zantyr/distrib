import signal
import sys

import actor
import processor

USAGE="""
"""

MAINPR = processor.MainProcessor

if __name__ == '__main__':
    try:
        if sys.argv[1]=='client':
            sole_actor = actor.Actor(targetProcessor=MAINPR)
            signal.pause()
        elif sys.argv[1]=='server':
            if '-r' in sys.argv[2:]:
                command = ' '.join([(sys.argv.index('-r')+1):])
                console = actor.Console(targetProcessor=MAINPR,cmd=command)
            else:
                console = actor.Console(targetProcessor=MAINPR)
            signal.pause()
        else:
            print "Please choose either client or server functionality"
    except IndexError:
        print USAGE
