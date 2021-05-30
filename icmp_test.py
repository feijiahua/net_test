import sys
import socket
from impacket import ImpactPacket, ImpactDecoder


def ICMP():
    dst = sys.argv[1]
    ip = ImpactPacket.IP()
    icmp = ImpactPacket.ICMP()

    icmp.set_icmp_type(8)
    icmp.set_icmp_code(0)
    icmp.set_icmp_id(12)
    icmp.set_icmp_cksum(0)
    icmp.auto_checksum = 1

    ip.contains(icmp)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    ip.set_ip_dst(dst)

    s.sendto(ip.get_packet(), (dst, 0))


if __name__ == '__main__':
    ICMP()
