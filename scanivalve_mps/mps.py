from scanivalve_mps.tcp import tcp_connect, tcp_sendrecv
from datetime import datetime

MPS_STATUSES = ['ready', 'scan', 'cal', 'val', 'calz', 'calm']

class MPS():
    def __init__(self, host: str, port: int):
        str: self.host = host
        int: self.port = port
        self.sock = tcp_connect(host, port)

    def bootloader_version(self) -> str:
        return tcp_sendrecv(self.sock, 'blver')

    def connect(self):
        self.sock = tcp_connect(self.host, self.port)

    def disconnect(self):
        self.sock.close()

    def get_time(self) -> datetime:
        data = tcp_sendrecv(self.sock, 'gettime').split()
        #print(data)
        datestr, timestr = data[2], data[3]
        year, month, day = [int(s) for s in datestr.split('/')]
        hour, minute, second = [int(s.split('.')[0]) for s in timestr.split(':')]
        sec, ns = int(data[5]), int(data[7])
        us = ns // 1000
        time = datetime(year, month, day, hour, minute, second, us)
        return time

    def set_time(self, time: datetime):
        """Sets the time on the MPS to the input value.
        If no error, returns the new time from the MPS."""
        #TODO currently only setting time up to a second precision
        #TODO expand to set nanoseconds field as well
        timestr = time.strftime('%Y/%m/%d %H:%M:%S')
        data = tcp_sendrecv(self.sock, 'settime ' + timestr)
        #print('IN SETTIME: ', data)
        if 'ERROR' in data:
            raise ValueError(data)
        return self.get_time()

    def status(self):
        data = tcp_sendrecv(self.sock, 'status')
        stat = data.split()[1].lower()
        if not stat in MPS_STATUSES:
            raise ValueError('Bad status returned from MPS')
        else:
            return stat

