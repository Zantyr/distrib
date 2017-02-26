import threading

INTERPRETERS = {
'mock':lambda self,code:"Code completed!"
}

class Deferred(object):
    def __init__(self,outbox,digest,requester,lang,code):
        self.outbox = outbox
        self.requester = requester
        self.interpreter = INTERPRETERS[lang]
        self.code = code
        self.digest = digest
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    def run(self):
        content = self.interpreter(self.code)
        self.outbox.append((self.requester,
             "RPROM!{}\0{}".format(self.digest,content)))
