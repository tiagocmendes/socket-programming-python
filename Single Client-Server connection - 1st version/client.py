from socket import *
import json
from datetime import datetime

s = socket(AF_INET, SOCK_STREAM)    
s.connect(('localhost',1234))           # connect to server (block until accepted)
json_message = json.dumps({"timestamp": datetime.now().timestamp(),"nome":"Tiago Mendes","mensagem":"Hello World"})
s.send(json_message.encode('utf-8'))    # send some data
data = s.recv(1024).decode('utf-8')     # receive the response
print(data)                             # print the result
s.close()                               # close connection


