from scanivalve_mps.tcp import tcp_connect, tcp_sendrecv, tcp_encode, tcp_recvall
from datetime import datetime

MPS_AVAILABLE_UNITS = ['PSI', 'ATM', 'BAR', 'CMHG', 'CMH2O', 'DECIBAR', 
    'FTH2O', 'GCM2', 'INHG', 'INH2O', 'KNM2', 'KGM2', 'KGCM2', 'KPA', 
    'KIPIN2', 'MPA', 'MBAR', 'MH2O', 'MMHG', 'NM2', 'NCM2', 'OZIN2', 
    'OZFT2', 'PA', 'PSF', 'TORR', 'USER', 'RAW']
MPS_FPS_MAX = 4294967295 # 2**32 - 1
MPS_STATUSES = ['ready', 'scan', 'cal', 'val', 'calz', 'calm']


class MPS():
    def __init__(self, host: str, port: int = 23):
        str: self.host = host
        int: self.port = port
        self.sock = tcp_connect(host, port)

    def bootloader_version(self) -> str:
        return tcp_sendrecv(self.sock, 'blver')

    def calibrate_zero(self) -> None:
        """Starts a zero calibration and 
        places the MPS4000 into CALZ mode."""
        data = tcp_sendrecv(self.sock, 'calz')
        return

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
        """Starts scanning and places the MPS4264 into SCAN mode.
        Returns the final data as a list of strings records."""
        return tcp_sendrecv(self.sock, 'scan')

    def scan_to_csv(self, filename):
        """Starts scanning and places the MPS4264 into SCAN mode.
        Stores the data into a CSV file."""
        data = tcp_sendrecv(self.sock, 'scan')
        with open(filename, 'w') as f:
            f.write('\n'.join(data))
        return

    def set_frames_per_scan(self, fps: int):
        """Set the number of frames in a scan."""
        if fps < 0 or fps > MPS_FPS_MAX:
            raise ValueError('frames per scan must be 0 <= fps <= ' + str(MPS_FPS_MAX))
        data = tcp_sendrecv(self.sock, 'set fps ' + str(fps))
        return

    def set_format(self, format_code):
        """Set the format of the scanned data."""
        if not format_code in ['ascii', 'formatted_ascii', 'csv']:
            raise ValueError('format_code must be ascii, formatted_ascii, or csv')
        data = tcp_sendrecv(self.sock, 'set format t ' + format_code[0])
        return

    def set_rate(self, rate: float):
        """Set the scan rate in samples/channel/second (Hz)."""
        if not 0.25 < rate < 850:
            raise ValueError('rate must be 0.25 < rate < 850')
        data = tcp_sendrecv(self.sock, 'set rate ' + str(rate))
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

    def set_scan_units(self, units: str) -> None:
        """Sets the scan units. See MPS_AVAILABLE_UNITS for accepted values."""
        data = tcp_sendrecv(self.sock, 'set units ' + units)
        return

    def status(self):
        data = tcp_sendrecv(self.sock, 'status')
        stat = data.split()[1].lower()
        if not stat in MPS_STATUSES:
            raise ValueError('Bad status returned from MPS')
        else:
            return stat

    def stop(self):
        """Cancels all commands and returns MPS4000 to Ready mode."""
        data = tcp_sendrecv(self.sock, 'stop')
        return

    def stream(self, frames=50):
        """Starts a scan and streams data to the terminal."""
        self.sock.sendall(tcp_encode('scan'))
        for i in range(frames):
            print(tcp_recvall(self.sock))
        self.sock.sendall(tcp_encode('stop'))

    def version(self):
        return tcp_sendrecv(self.sock, 'ver')
