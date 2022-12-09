import socket
from _thread import *
import threading

destination_folder = "FilesRecieved\\"

print_lock = threading.Lock()


def receive_file(client):

    filename, filesize, size_a, size_r = client.recv(4096).decode().strip().split("|")

    with open(f"{destination_folder}{filename}", "wb") as f:
        for i in range(int(size_a)):
            bytes_read = client.recv(4096)
            f.write(bytes_read)
        bytes_read = client.recv(int(size_r))
        f.write(bytes_read)
        print("file recieved")


# thread function
def threaded(c):
    while True:
        print("a")
        receive_file(c)
        print("b")


    # connection closed
    c.close()


def Main():
    host = ""

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
