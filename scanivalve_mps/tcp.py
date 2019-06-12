"""
tcp.py -- Helper functions to send and receive TCP messages.
"""
import socket
import time

BUFFER_SIZE = 4096


def str_to_tcp(string):
    """Encode string to TCP message."""
    return string.encode() + b'\r\n'


def tcp_to_str(message):
    """Decode TCP message to string."""
    string = message.decode().split('\r\n')
    if string[-1] == '' or string[-1] == '>':
        string = string[:-1]
    return string


def tcp_recvall(sock):
    """Streams incoming data from the socket
    until the whole message is received."""
    data = b''
    while True:
        packet = sock.recv(BUFFER_SIZE)
        data += packet
        if len(packet) < BUFFER_SIZE:
            break
    return data


def tcp_sendrecv(sock, message):
    """Sends a TCP message to socket.
    Returns a decoded and stripped response message."""
    sock.sendall(str_to_tcp(message))
    data = tcp_to_str(tcp_recvall(sock))
    if len(data) == 1:
        data = data[0]
    return data


def tcp_connect(host, port):
    """Thin wrapper around socket.connect(). 
    Takes a host string (IP address) and port number, 
    and returns a socket instance."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock
