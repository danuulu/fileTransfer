import os
import socket
import struct

IP = socket.gethostbyname(socket.gethostname())
PORT = 4460
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def send_file(sck: socket.socket, filename):
                # Get the size of the outgoing file.
                print(filename)
                filesize = os.path.getsize(filename)
                # First inform the server the amount of
                # bytes that will be sent.
                sck.sendall(struct.pack("<Q", filesize))
                print("sent size")
                # Send the file in 1024-bytes chunks.
                with open(filename, "rb") as f:
                    while read_bytes := f.read(1024):
                        print("sendingd stuff")
                        sck.sendall(read_bytes)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        elif cmd == "UPLOAD":

            path = data[1]

            send_data = f"{cmd}@{path}@{path}"
            client.send(send_data.encode(FORMAT))
            send_file(client, path)

            # with open(f"{path}", "r") as f:
            #     text = f.read()
            #
            # filename = path.split("/")[-1]
            # send_data = f"{cmd}@{filename}@{text}"
            # client.send(send_data.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
