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

    def get_scan_start_time(self) -> datetime:
        """Gets the start time of the last scan as 
        yyyy/mm/dd hh:mm:ss.nnnnnn. This command is valid in all modes.
        If no scan has been run since power up the following time is 
        returned: 2015/1/1 0:0:0.000000."""
        data = tcp_sendrecv(self.sock, 'sst').split()
        datestr, timestr = data[0], data[1]
        year, month, day = [int(s) for s in datestr.split('/')]
        hour, minute, second = [int(s.split('.')[0]) for s in timestr.split(':')]
        ns = int(data[1][9:]) // 1000
        time = datetime(year, month, day, hour, minute, second, ns)
        return time

    def get_time(self) -> datetime:
        """Gets the current PTP time as used by the MPS.
        Time is adjusted by mps.utc_offset()."""
        data = tcp_sendrecv(self.sock, 'gettime').split()
        datestr, timestr = data[2], data[3]
        year, month, day = [int(s) for s in datestr.split('/')]
        hour, minute, second = [int(s.split('.')[0]) for s in timestr.split(':')]
        sec, ns = int(data[5]), int(data[7])
        us = ns // 1000
        time = datetime(year, month, day, hour, minute, second, us)
        return time

    def scan(self):
        """Starts scanning and places the MPS4264 into SCAN mode."""
        return tcp_sendrecv(self.sock, 'scan')

    def set_format(self, format_code):
        """Set the format of the scanned data."""
        if not format_code in ['ascii', 'formatted_ascii', 'csv']:
            raise ValueError('format_code must be ascii, formatted_ascii, or csv')
        data = tcp_sendrecv(self.sock, 'set format t ' + format_code[0])
        return

    def set_time(self, time: datetime) -> datetime:
        """Sets the time on the MPS to the input value.
        If no error, returns the new time from the MPS."""
        #TODO currently only setting time up to a second precision
        #TODO expand to set nanoseconds field as well
        timestr = time.strftime('%Y/%m/%d %H:%M:%S')
        data = tcp_sendrecv(self.sock, 'settime ' + timestr)
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

    def version(self):
        return tcp_sendrecv(self.sock, 'ver')
