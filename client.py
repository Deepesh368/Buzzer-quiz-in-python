import socket
import select
import sys
from inputimeout import inputimeout, TimeoutOccurred

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', 1234))


def give_reply():
    try:
        something = inputimeout(prompt='Waiting for input: ', timeout=10)
        return(something)
    except TimeoutOccurred:
        print("Time Up!")
        return("N")


while True:
    sockets_list = [server]
    r, w, error = select.select(sockets_list, [], [])
    for socks in r:
        if socks == server:
            message = str(socks.recv(100).decode())
            if(message is "1"):
                answer = str(give_reply())
                server.send(bytes(answer, "utf-8"))
            else:
                print(message)
server.close()
sys.exit()
