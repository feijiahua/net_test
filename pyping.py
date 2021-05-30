import sys
import time
import socket
import struct
import getopt
import argparse
from impacket import ImpactDecoder, ImpactPacket


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
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht")
    except getopt.GetoptError:
        print('Inout error')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('pyping <dst ip>')
            sys.exit(0)

    dst = args[0]
    send_and_recv(dst)


class Ping():
    def __init__(self):
        pass


if __name__ == '__main__':
    pyping()
