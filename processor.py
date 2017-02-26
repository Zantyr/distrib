import os
import threading
import time

import promise
import deferred

class Processor(object):
    def __init__(self,inbox,outbox,env):
        """
        This object processes messages. Looks into inbox, picks a msg,
        and returns processed msg into the outbox. Has internal state, which
        dictates what messages to look.
        """
        self.inbox = inbox
        self.outbox = outbox
        self.environment = env
        self.thread = threading.Thread(target=self.execute)
    def execute(self):
        """
        Method passed to thread after its instantiation. Does the real processing
        """
        while True:
            try:
                item = self.inbox.popleft()
                self.process(item)
            except IndexError:
                time.sleep(0.1)

    def process(self,item):
        """
        Processor implementations fill this method
        """
        raise NotImplementedError

    def run(self):
        self.thread.start()

    def interrupt(self,signal):
        """
        Interrupts the processor, may cancel or suspend transaction.
        Is superior to any other computation on the processor.
        Interrupts are queuable
        """
        raise NotImplementedError


class MockProcessor(Processor):
    def process(self,item):
        print "{} received: {}".format(id(self),item)




class MainProcessor(Processor):
    def process(self,item):
        if item[:4] == "MSG\x00":
            print item[4:]+"\n"

        elif item[:6] == "GFILE!":
            name,content = item[6:].split('\0',1)
            with open("download{}{}".format(os.sep,name), "w") as f:
                f.write(content)

        elif item[:6] == "SFILE!":
            name,user = item[6:].split('!',1)
            if os.path.isfile("download{}{}".format(os.sep,name)):
                    with open("download{}{}".format(os.sep,name),'r') as f:
                        msg = "GFILE!{}\0{}".format(name,f.read())
                    self.outbox.append((user,msg))
            else:
                    print "No file: download{}{}".format(os.sep,name)
                    #Zwraca wyslanemu brak pliku. Outbox powinien informowac o braku pliku.
        #promises: local
        #deferred: remote
        elif item[:6] == "CPROM!": #createPromise
            lang,executor,receiver,code == item[6:].split('\0',3)
            digest = str(hash(item))
            self.environment["P"+digest] = promise.Promise(executor,lang,code)
            self.outbox.append((executor,
                "RDEFR!{}\0{}\0{}\0".format(lang,receiver,digest,code)))
        elif item[:6] == "RDEFR!": #receiveDeferred
            lang,requester,digest,code == item[6:].split('\0',3)
            dfr = deferred.Deferred(self.outbox,digest,requester,lang,code)
            self.environment["D"+digest] = dfr
        elif item[:6] == "RPROM!": #receivePromise
            id,content = item[6:].split('\0',1)
            self.environment["P"+id].fulfill(content)
