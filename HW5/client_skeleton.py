#!/usr/bin/env python3

import sys
import string
import random
import time
import hashlib
import socket
import binascii

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from bitarray import bitarray

char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

AES_KEY_SIZE = 32
AES_IV_SIZE  = AES.block_size
AES_MODE     = AES.MODE_CBC

CHAT_MSG_LEN        = 64
CHAT_MSG_BODY_LEN   = 44
CHAT_MSG_INDEX_LEN  = 20
NUMBER_OF_CHAT_MSGS = 10

PRIMARY_SERVER_ID = 0

class ServerData:

    server_id  = None
    public_key = None
    shared_key = None
    server_ip  = None
    udp_port   = None

    def __init__(self, server_id, public_key, shared_key, server_ip, udp_port):

            self.server_id  = server_id
            self.public_key = public_key
            self.shared_key = shared_key
            self.server_ip  = server_ip
            self.udp_port  = udp_port

def read_server_data():

    # Read data about the servers from a file
    servers_filename = 'all_servers.txt'

    all_servers = []
    with open(servers_filename, 'r') as fp:

        for line in fp.readlines():
            server_id = int(line.split()[0])
            server_ip = line.split()[1]
            udp_port  = int(line.split()[2])

            all_servers.append(ServerData(server_id, None, None, server_ip, udp_port))

    return all_servers

# Onion encrypt provided message, with server shared keys in reverse order.
# result = enc_km(...enc_k1(enc_k0(msg))...)
# Encryption algorithm: AES
# Encryption mode: AES_MODE = AES.MODE_CBC
# Docs: https://www.dlitz.net/software/pycrypto/api/current/Crypto-module.html
# Example of AES encryption:
#   iv = Random.new().read(AES_IV_SIZE)
#   cipher = iv + AES.new(key, AES_MODE, iv).encrypt(plain)
def onion_encrypt_message(msg, servers):

    # TODO: in
    reversed_servers = servers[::-1]

    cipher_msg = msg
    for server in reversed_servers:
        iv = Random.new().read(AES_IV_SIZE)
        cipher_msg = iv + AES.new(server.shared_key, AES_MODE, iv).encrypt(cipher_msg)

    return cipher_msg

# Onion decrypt provided ciphertext
# See the explanation for the ecnryption
def onion_decrypt_message(cip, servers):

    # TODO: insert your code here!
    for server in servers:
        iv = cip[:AES_IV_SIZE]
        cip = AES.new(server.shared_key, AES_MODE, iv).decrypt(cip[AES_IV_SIZE:])

    return cip

def rsa_encrypt(msg, pub_key):

    return pub_key.encrypt(msg, None)[0]

# Sends a message to the server
# Important: Expects a response from the server
# Input argument msg should be a string
def send_msg_to_server(server, msg):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (server.server_ip, server.udp_port))

    data = None
    sock.settimeout(1)
    try:
        data, other = sock.recvfrom(4096)
    except socket.timeout:
        print('UDP receive request from server %d timed-out' % server.server_id)
    finally:
        sock.close()

    return data

# Sends a message to the server
# Doesn't expect a response from server
# Input argument msg should be a string
def send_msg_to_server_async(server, msg):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (server.server_ip, server.udp_port))
    sock.close()

def generate_random_message(msg_len):

    return ''.join([random.choice(char_set) for _ in range(msg_len)])

# Generates random chat messages of the following format:
# first CHAT_MSG_INDEX_LEN characters represent msg index
# next  CHAT_MSG_BODY_LEN characters are the message itself
def generate_chat_messages(num_msg):

    messages = []
    for i in range(num_msg):
        msg = generate_random_message(CHAT_MSG_BODY_LEN)
        msg_idx = str(i).zfill(CHAT_MSG_INDEX_LEN)

        messages.append(msg_idx + msg)

    return messages

# Client which is responsible for:
#   - Generate and send a shared key to each server
#   - Generate chat messages, onion-encrypt them and
#     send them to the primary server
def client_sender(servers, num_messages):

    # Generate and exchange AES shared key with each server
    # Generated shared key should be encrypted with server's
    # public key before sending (see server_skeleton script
    # for the expected format of shared key)
    # TODO: insert your code here!
    for server in servers:
        random_key = generate_random_message(AES_KEY_SIZE)
        key = hashlib.sha256(random_key.encode()).digest()
        iv = Random.new().read(AES.block_size)
        AES_cipher_key = iv + AES.new(server.public_key, AES_MODE, iv).encrypt(key)
        send_msg_to_server_async(server, 'shared_key '+ AES_cipher_key)

    # Generate and onion-encrypt messages
    messages = generate_messages(num_messages)
    messages_enc = []
    for m in messages:
        messages_enc.append(onion_encrypt_message(m, servers))

    # Send onion-encrypted messages to the primary server
    # See server_skeleton script for the expected format of a messsage
    # TODO: insert your code here!
    primary_server = [server for server in servers if server['server_id']==PRIMARY_SERVER_ID][0]
    for message_enc in messages_enc:
        send_msg_to_server_async(primary_server, 'chat_msg_client ' + message_enc)

# Client which is responsible for making the PIR
# It should generate appropriate random masks for each server,
# send the pir requests and finally recover the target message
# Target message is the one with the provided target_msg_index
def client_receiver(servers, num_messages, target_msg_index):

    # TODO: insert your code here!
    masks = []
    final_mask_str = ['0' for i in range(num_messages)]
    final_mask_str[target_msg_index] = '1'
    final_mask_str = "".join(final_mask)
    final_mask = bitarray(final_mask_str)

    # Logic Description
    # xored = ((final_mask ^ m1) ^ m2) ^ m3
    #
    # and back
    # final_mask = ((xored ^ m3) ^ m2) ^ m1
    previous_mask = final_mask
    for server in servers:
        mask_str = [str(random.randint(0,1)) for i in range(num_messages)]
        random_mask = bitarray("".join(mask_str))

        mask = previous_mask ^ random_mask
        masks.append(mask)

        messages_as_bytes = send_msg_to_server(server, 'pir_req '+ mask.to01())

        # TODO Not sure here
        # we get the set of messages as bytes from different servers but frankly
        # we dont care about all those messages where indx doesnt match
        # I guess we need to convert message as bytes back to list of dicts [{1:'asda'}, {2:'bas'}]
        # find our message and return (but send masks to each server nontheless)

        previous_mask = mask

    # Return the target message (string), only the body of the message,
    # without the message index
    return result


# This function is for your convinience, so you could tets your solution localy
# Feel free to write your own test functions, this is just an example
def test_function():

    all_servers = read_server_data()

    messages = client_sender(all_servers, NUMBER_OF_CHAT_MSGS)

    print('Allow servers some time to exchange the messages')
    time.sleep(5)

    target_msg_index = random.randrange(NUMBER_OF_CHAT_MSGS)

    res = client_receiver(all_servers, NUMBER_OF_CHAT_MSGS, target_msg_index)

    for s in all_servers:
        send_msg_to_server_async(s, 'quit')

    target = messages[target_msg_index]

    if res == target[CHAT_MSG_INDEX_LEN:]:
        print('Success')
    else:
        print('Failure')



# This is the function which should be called when you upload your solution
# Your script will be provided with one cmd line argument, which is the index
# of the target message that you should recover with PIR
# Don't change this function!
def grading_main():

    if len(sys.argv) != 2:
        print('Wrong number of commmand line arguments')
    else:
        target_index = int(sys.argv[1])

        all_servers = read_server_data()

        result = client_receiver(all_servers, NUMBER_OF_CHAT_MSGS, target_index)

        print(result)


if __name__ == '__main__':

    # Feel free to replace the function and insert your own tests here
    # while you test your solution localy,
    # but when you want to upload your script for grading,
    # make sure this is the function which is called here!
    grading_main()
