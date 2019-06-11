from scanivalve_mps.tcp import tcp_connect, tcp_sendrecv

HOST = '191.30.90.1'
PORT = 23

sock = tcp_connect(HOST, PORT)
print(tcp_sendrecv(sock, 'blver'))
sock.close()
