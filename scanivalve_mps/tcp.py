"""
tcp.py -- Helper functions to send and receive TCP messages.
"""
import socket

BUFFER_SIZE = 4096


def str_to_tcp(string):
    """Encode string to TCP message."""
    return string.encode() + b'\r\n'


def tcp_to_str(message):
    """Decode TCP message to string."""
    string = message.decode()
    if string[-1] == '>':
        return string.rstrip('\r\n>')
    else:
        return string.rstrip('\r\n')


def tcp_sendrecv(sock, message):
    """Sends a TCP message to socket.
    Returns a decoded and stripped response message."""
    sock.sendall(str_to_tcp(message))
    return tcp_to_str(sock.recv(BUFFER_SIZE))


def tcp_connect(host, port):
    """Thin wrapper around socket.connect(). 
    Takes a host string (IP address) and port number, 
    and returns a socket instance."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock
