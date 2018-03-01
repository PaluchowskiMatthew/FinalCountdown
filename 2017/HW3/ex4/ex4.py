from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests
import binascii
import base64

global counter

def print_raw_bytes(pkt):
    print(pkt.get_payload())

def parse_raw_and_accept(raw):
    ip = IP(raw)

    if ip.haslayer(TCP) and ip.getlayer(TCP).dport == 443:
        tcp = ip[TCP]

        if tcp.haslayer(Raw):
            http_content = tcp.getlayer(Raw).load

            if re.search('\x16\x03\x02',http_content.decode('ISO-8859-5'),flags=0): # TLS 1.2
                print('drop1')
                return False
            elif re.search('\x16\x03\x03',http_content.decode('ISO-8859-5'),flags=0): #TLS 1.3
                print('drop2')
                return False
            else:
                print('accept')
                return True

        return True

    return True



def print_layers(raw):
    pkt = IP(raw)
    layers = []
    counter = 0
    while True:
        layer = pkt.getlayer(counter)
        if (layer != None):
            # print(layer.name)
            layers.append(layer.name)
        else:
            break
        counter += 1

    print("Layers are:\t\t",layers)

def new_pkt(pkt):
    raw = pkt.get_payload()
    ip = IP(raw)
    new_packet = IP(dst=ip[IP].dst, src=ip[IP].src)/TCP()
    new_packet[TCP].sport = ip[TCP].sport
    new_packet[TCP].dport = ip[TCP].dport
    new_packet[TCP].seq = ip[TCP].seq
    new_packet[TCP].ack = ip[TCP].ack
    new_packet[TCP].flags = 'AF'
    print(new_packet.summary())
    send(new_packet)

def intercept(pkt):
    raw = pkt.get_payload()
    ip = IP(raw)
    print(ip.summary())

    if not parse_raw_and_accept(pkt.get_payload()):
        pkt.drop()
    else:
        pkt.accept()


def print_and_accept(pkt):
    parse_raw(pkt.get_payload())
    pkt.accept()

def print_and_drop(pkt):
    print_layers(pkt.get_payload())
    pkt.drop()


nfqueue = NetfilterQueue()
nfqueue.bind(0, intercept, 100)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
