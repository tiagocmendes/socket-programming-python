from socket import *
import json
from datetime import datetime

import sys
import fcntl
import os 
import selectors

print("----------------------------------------")
print("DISTRIBUED SYSTEMS CHAT")
print("Socket programming using Python")
print("----------------------------------------")
name = input("Please, type your name: ")
print("Welcome, " + name + "!")


# set sys.stdin non-blocking
orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

s = socket(AF_INET, SOCK_STREAM)    
host = '127.0.1.1'
port = 1234
s.connect((host,port))           # connect to server (block until accepted)

# function to be called when enter is pressed
def got_keyboard_data(stdin):
    line = stdin.read()
    now = datetime.now().timestamp()
    if "quit" in str(line): 
        json_message = json.dumps({"timestamp": now,"nome":name,"mensagem":"{} left the chat.".format(name)})
        s.send(json_message.encode('utf-8'))
        print(name + " left the chat.")     # close connection
        s.close()
        sys.exit(0)
    print("> " + name + ": " + str(line).replace("\n", "") + " (" + str(now) + ")")
    json_message = json.dumps({"timestamp": now,"nome":name,"mensagem":line})
    s.send(json_message.encode('utf-8'))

def read_socket(s):
    data = s.recv(1024).decode('utf-8')     # receive the response
    json_message = json.loads(data)
    print("\n> " + json_message['nome'] + ": " + str(json_message['mensagem']).replace("\n", "") + " (" + str(json_message['timestamp']) + ")")

# register event
m_selector = selectors.DefaultSelector()
m_selector.register(sys.stdin, selectors.EVENT_READ, got_keyboard_data)
m_selector.register(s, selectors.EVENT_READ, read_socket)

while True:
    sys.stdout.write('Type something and hit enter: ')
    sys.stdout.flush()
    for k, mask in m_selector.select():
        callback = k.data
        callback(k.fileobj)


