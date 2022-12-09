import socket
import copy
import sys
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time


def send_file(filename, server):
    def handshake():
        # Notify the server that a file is sending
        server.send("Sending File...".encode())
        # Receive Server Acknowledgment
        if not server.recv(48).decode() == "Receiving File.":
            print("Server Acknowledgement Failed")
            return "Server Acknowledgment Failed"
        return None

    if (error := handshake()) is not None:
        print(error)
        return

    # Get the filesize of the file
    filesize = os.stat(filename).st_size
    # If open(filename, "type").read(bytesize) doesn't get the same number of bytes
    # it just hangs there waiting
    # Solution: calculate how many times we send 4096 bytes then send the remainder
    # the server will do the same on it's end
    size_a = filesize // 4096
    size_r = filesize % 4096

    # Save the filename, file size, number of 4096 bytes, and remainder
    format_filename = f"{copy.copy(filename)}|{filesize}|{size_a}|{size_r}"
    filename_size = sys.getsizeof(format_filename.encode())
    # After sending acknowledgement, server expects a byte size of 4096 bytes
    # Make the filename 4096 bytes
    if filename_size < 4096:
        for i in range(4096-filename_size):
            format_filename += " "
    # Send the filename, file size, number of 4096 bytes, and remainder to the server
    server.send(format_filename.encode())

    # Give the server some time to process
    time.sleep(1)

    # Send the file
    with open(filename, "rb") as f:
        for i in range(size_a):
            bytes_read = f.read(4096)
            server.sendall(bytes_read)
        bytes_read = f.read(size_r)
        server.sendall(bytes_read)
        print("File sent")

    # The server is supposed to send "File {filename} {bytesize} bytes received"
    print(server.recv(4096).decode().strip())


def on_created(event):
    pass


def main():
    # Watchdog initialization code
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = None
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = "Camera\\Images"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    print("im here")

    # define server location (localhost)
    host = "127.0.0.1"
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to Server
    s.connect((host, port))




if __name__ == "__main__":
    main()
