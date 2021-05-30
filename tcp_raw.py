#!/usr/bin/env python

import sys
import socket
from impacket import ImpactDecoder, ImpactPacket


def main():
    if len(sys.argv) < 3:
        print("Use: %s <src ip> <dst ip>" % (sys.argv[0]))
        print("Use: %s <src ip> <dst ip> <cnt>" % (sys.argv[0]))
        sys.exit(1)

    elif len(sys.argv) == 3:
        src = sys.argv[1]
        dst = sys.argv[2]
        cnt = 1

    elif len(sys.argv) == 4:
        src = sys.argv[1]
        dst = sys.argv[2]
        cnt = sys.argv[3]

    else:
        print("Input error!")
        sys.exit(1)

    ip = ImpactPacket.IP()
    ip.set_ip_src(src)
    ip.set_ip_dst(dst)

    icmp = ImpactPacket.ICMP()
    tcp = ImpactPacket.TCP()
    tcp.set_th_sport(55968)
    tcp.set_th_dport(80)
    tcp.set_th_seq(1)
    tcp.set_th_ack(1)
    tcp.set_th_flags(0x18)
    tcp.set_th_win(64)

    tcp.contains(ImpactPacket.Data())

    ip.contains(tcp)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    seq_id = 0

    while(cnt >= 1):
        seq_id = seq_id + 1
        tcp.set_th_seq(seq_id)
        tcp.calculate_checksum()

        s.sendto(ip.get_packet(), (dst, 80))
        cnt -= 1


if __name__ == '__main__':
    main()
