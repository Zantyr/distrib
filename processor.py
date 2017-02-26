import os
import threading

class Processor(object):
    def __init__(self,inbox,outbox):
        """
        This object processes messages. Looks into inbox, picks a msg,
        and returns processed msg into the outbox. Has internal state, which
        dictates what messages to look.
        """
        self.inbox = inbox
        self.outbox = outbox
        self.thread = threading.Thread(target=self.execute)
    def execute(self):
        """
        Method passed to thread after its instantiation. Does the real processing
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
    def execute(self):
        while True:
            try:
                item = self.inbox.popleft()
                print "{} received: {}".format(id(self),item)
            except IndexError:
                pass




class MainProcessor(Processor):
    def execute(self):
        while True:
            try:
                item = self.inbox.popleft()
                if item[:4] == "MSG\x00":
                    print item[4:]+"\n"

                elif item[:6] == "GFILE!":
                    name,content = request[6:].split('\0',1)
                    with open("download{}{}".format(os.sep,name), "w") as f:
                        f.write(content)

                elif item[:6] == "SFILE!":
                    name,ipaddr = item[6:].split('!',1)
                    if os.path.isfile("download{}{}".format(os.sep,name)):
                         with open("download{}{}".format(os.sep,name),'r') as f:
                             msg = "GFILE!{}\0{}".format(name,f.read())
                         self.outbox.append((name,msg))
                    else:
                         self.outbox.append((None, addr))
                         #Zwraca wyslanemu brak pliku. Outbox powinien informowac o braku pliku.

            except IndexError:
                pass
