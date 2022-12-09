# Import socket module
import socket


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    filename = "abc16.jpg"
    while True:

        # send filename to server
        s.send(filename.encode())
        print(f"filename {filename} sent")

        data = s.recv(4096)
        if data:
            print(data.decode())
        #send file data to server
        with open(filename, "rb") as f:
            print("im here")
            while True:
                # read the bytes from the file
                bytes_read = f.read(4096)
                if not bytes_read:
                    print("file transmission done")
                    break
                # we use sendall to assure transimission in
                # busy networks
                s.sendall(bytes_read)
            s.sendall("File transmission done".encode())

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
