class test(processor):
    def execute(self):
        while True:
            try:
                item = self.inbox.popleft()
                if item[:4] == "MSG\x00"
                    print item[5:]
                elif item[:6] == "GFILE!"
                    name = ""
                    for i in range(7, len(item)):
                        if item[i] != "\x00":
                            name+=item[i]
                            #szuka pustego bitu, dodaje nazwe
                        else:
                            #tworzy plik
                            with open("download\\%s" % name, "wb") as f:
                                f.write(item[i+1:])
                                f.close()
                            break
                elif item[:6] == "SFILE!":
                    raise NotImplementedError
            except IndexError:
                pass
