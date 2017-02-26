import actor
import signal

CLIENT = False

if __name__ == '__main__':
    if CLIENT:
        sole_actor = actor.Actor(targetProcessor=actor.MockProcessor)
    else:
        console = actor.Console(targetProcessor=actor.MockProcessor)
    signal.pause()