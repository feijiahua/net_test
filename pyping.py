import os
import sys
import time
import signal
import errno
import socket
import struct
import getopt
import argparse
from functools import wraps
from impacket import ImpactDecoder, ImpactPacket

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

def log(func):
    def wrapper(*args, **kargs):
        print('log')
        return func(*args, **kargs)
    
    return wrapper


@timeout(5)
def send_and_recv(dst):
    ip = ImpactPacket.IP()
    icmp = ImpactPacket.ICMP()

    icmp.set_icmp_type(8)
    icmp.set_icmp_code(0)
    icmp.set_icmp_id(12)
    icmp.contains(ImpactPacket.Data(b'ping test'))
    icmp.set_icmp_cksum(0)
    icmp.auto_checksum = 1

    ip.contains(icmp)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    ip.set_ip_dst(dst)

    send_time = time.time()
    s.sendto(ip.get_packet(), (dst, 0))
    ip, (src_ip, _) = s.recvfrom(1500)
    recv_time = time.time()
    recv = ip[20:]
    id = struct.unpack('!H', recv[4:6])[0]
    seq = struct.unpack('!H', recv[6:8])[0]
    len = struct.unpack('!H', ip[2:4])[0] - 20
    wast_time = recv_time - send_time
    print('%d bytes from %s: icmp_seq=%d id=%d time=%fms' %
          (len, src_ip, seq, id, wast_time))


def pyping():
    always = False

    parser = argparse.ArgumentParser(description="use for pyping")
    # 必选参数
    parser.add_argument('ip', help='the dst ip')
    # 可选参数
    parser.add_argument('--version', '-v', action='version', version='%(prog)s version: v 0.01', help='show the version')
    # 互斥参数
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--count', help='Stop after sending count ECHO_REQUEST packets. With deadline option, ping waits for count ECHO_REPLY packets, until the timeout expires.')
    group.add_argument('-t', action="store_true")

    args = parser.parse_args()
    dst = args.ip

    if args.t:
        while True:
            try:
                send_and_recv(dst)
                time.sleep(1)
            except TimeoutError:
                print('timeout')
    elif args.count:
        cnt = int(args.count)
        while cnt:
            try:
                send_and_recv(dst)
                time.sleep(1)
            except TimeoutError:
                print('timeout')
            finally:
                cnt -= 1
    


class Ping():
    def __init__(self):
        pass


if __name__ == '__main__':
    pyping()
