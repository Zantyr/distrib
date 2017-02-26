class Promise(object):
    def __init__(self,executor,lang,code):
        self.executor = executor
        self.lang = lang
        self.code = code
        self.content = None
    def fulfill(self,content):
        self.content = content
