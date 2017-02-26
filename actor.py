from collections import deque
import socket
import sys
import threading

class Actor(object):
    def __init__(self,threads=5,targetProcessor=None,bind_port=1488,bind_ip="0.0.0.0",
            address_book=None):
        self.inbox = deque()
        self.outbox = deque()
        self.sender = threading.Thread(target=self.send)
        self.receiver = threading.Thread(target=self.recv)
        self.threadpool = [targetProcessor(self.inbox, self.outbox) for x in range(threads)]
        self.addressbook = ({key:tuple(val) for key,val in address_book.items()}
            if address_book else {})
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.sender.start()
        self.receiver.start()
        [x.run() for x in self.threadpool]
        print "Actor started"

    def send(self):
        """
        Loop over mailbox and dispatch the messages.
        Archive the messages if did not sent
        """
        while True:
            try:
                (target,message) = self.outbox.popleft()
                if type(target)==str:
                    target_ip,target_port = self.addressbook[target]
                else:
                    target_ip,target_port = target
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((target_ip, target_port))
                client.send(message)
                resp = client.recv(4096)
                #what to do with response?
            except IndexError:
                pass
            except KeyError:
                pass    #there is no target in the addressbook
            except socket.error as e:
                print "Socket Error occured: {}".format(e.errno)

    def recv(self):
        """
        Listen on tcp/ip port and put the messages into the inbox
        """
        self._serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._serv.bind((self.bind_ip, self.bind_port))
        self._serv.listen(5)
        while True:
            client,addr = self._serv.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()

    def handle_client(self,client_socket):
        """
        Internal processing of incoming TCP packets
        """
        #larger buffer for larger messages
        request = client_socket.recv(1024)
        self.inbox.append(request)
        client_socket.send("ACK!")
        client_socket.close()


class Console(Actor):
    def __init__(self,*args,**kwargs):
        """
        A master console: allows to control the threads, post problems to solve and manage the net
        """
        super(Console,self).__init__(*args,**kwargs)
        if 'cmd' not in kwargs:
            import readline
            while True:
                line = raw_input("xD -> ")
                self.parse(line)
        else:
            self.parse(self.kwargs['cmd'])
            sys.exit()

    def parse(self,line):
        try:
            line = line.split(' ',2)
            if line[0].lower() == 'quit':
                sys.exit()
            elif line[0].lower() == 'add':
                tp = line[2].split(' ',1)
                self.addressbook[line[1]] = (tp[0],int(tp[1]))
            elif line[0].lower() == 'list':
                for key in self.addressbook:
                    print "{} has an address {}".format(key,str(self.addressbook[key]))
            elif line[0].lower() == 'send':
                 self.outbox.append((line[1],"MSG\0"+line[2]))
            elif line[0] == 'sendFile':
                 self.inbox.append("SFILE!{}!{}".format(line[2],line[1]))
            elif line[0] == 'outbox':
                 print self.outbox
        except IndexError:
            print "Console Syntax Error"
