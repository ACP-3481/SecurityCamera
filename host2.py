# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()


# thread function
def threaded(c):
    while True:
        received = c.recv(4096).decode()
        filename = received
        print(filename)
        c.send(f"Server receiving file: {filename}".encode())
        try:
            with open(f"ServerRecieved\\{filename}", "wb") as f:
                count = 1
                while True:
                    print(f"receiving file {count}")
                    count += 1
                    # read 1024 bytes from the socket (receive)
                    bytes_read = c.recv(4096)
                    try:
                        print(bytes_read.decode())
                        if bytes_read.decode() == "File transmission done":
                            print("file received")
                            break
                    except UnicodeDecodeError:
                        print("error")
                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        print("file received")
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
        except FileNotFoundError:
            pass

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
