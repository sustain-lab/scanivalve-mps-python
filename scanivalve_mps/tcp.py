"""
tcp.py -- Helper functions to send and receive TCP messages.
"""
from socket import socket, AF_INET, SOCK_STREAM
import time
from typing import List

BUFFER_SIZE: int = 4096


def tcp_decode(message: bytes) -> List:
    """Decode TCP message to a list of strings."""
    return message.decode().split('\r\n')[:-1]


def tcp_encode(string: str) -> bytes:
    """Encode string to TCP message."""
    return string.encode() + b'\r\n'


def tcp_recvall(sock: socket) -> bytes:
    """Streams incoming data from the socket
    until the whole message is received."""
    data = b''
    while True:
        packet = sock.recv(BUFFER_SIZE)
        data += packet
        if len(packet) < BUFFER_SIZE:
            break
    return data


def tcp_recvall_until_token(sock: socket, token: str) -> bytes:
    """Streams multiple TCP packets from the socket
    until we reach the input token."""
    data = b''
    while True:
        packet = tcp_recvall(sock)
        if packet.decode()[-1] == token:
            data += packet
            break
        else:
            data += packet
    return data


def tcp_sendrecv(sock: socket, message: str):
    """Sends a TCP message to socket.
    Returns a decoded and stripped response message."""
    sock.sendall(tcp_encode(message))
    data = tcp_decode(tcp_recvall_until_token(sock, '>'))
    if len(data) == 1:
        data = data[0]
    return data


def tcp_connect(host: str, port: int) -> socket:
    """Thin wrapper around socket.connect(). 
    Takes a host string (IP address) and port number, 
    and returns a socket instance."""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    return sock
