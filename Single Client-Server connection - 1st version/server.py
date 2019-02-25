from socket import *
import json
from datetime import datetime

s = socket(AF_INET, SOCK_STREAM)
s.bind(('localhost', 1234))
s.listen(100)
# s.setblocking(False)
(conn, addr) = s.accept()           # returns new socket and addr.
while True:                         # forever
    data = conn.recv(1024)          # receive data from client
    if not data: break              # stop if client stopped
    json_message = json.loads(data.decode('utf-8'))
    conn.send((str(json_message["timestamp"]) + " - " + json_message["nome"] + ": " + json_message["mensagem"]+"*").encode('utf-8'))        # return sent data plus an "*"
conn.close()                        # close the connection