import selectors
import socket

sel = selectors.DefaultSelector()

users = {}
last_port = None

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted',conn,'from',addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    last_port = addr[1]
    users[last_port] = conn


def read(conn, mask):
    data = conn.recv(1000)      # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        for port in users.keys():
            if users[port] != conn:
                users[port].send(data)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

# Create a Socket
def create_socket():
    try:
        global host
        global port 
        global sock
        host = str(socket.gethostbyname(socket.gethostname()))
        port = 1234
        sock = socket.socket()
        print("Server started! | IP: " + str(host) + " | Port: " + str(port))
    
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global sock
        print("Binding the Port: " + str(port))
        sock.bind((host, port))
        sock.listen(100)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
def accepting_connections():
    global host
    global port
    global sock
    while True:
        try:
            sock.setblocking(False)
            sel.register(sock, selectors.EVENT_READ,accept)
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)

        except:
            print("Error accepting connections")

# main function
def main():
    create_socket()
    bind_socket()
    accepting_connections()

# main call
main()

sock.close()