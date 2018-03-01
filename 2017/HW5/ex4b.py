#!/usr/bin/env python3

import sys
import string
import random
import time
import hashlib
import socket
import binascii
import ast

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

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

# https://stackoverflow.com/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python
def bytes_xor(a, b) :
    return bytes(x ^ y for x, y in zip(a, b))

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

    cipher_msg = msg.encode()
    for server in reversed_servers:
        iv = Random.new().read(AES_IV_SIZE)
        cipher_msg = iv + AES.new(server.shared_key, AES_MODE, iv).encrypt(cipher_msg)

    return binascii.hexlify(cipher_msg).decode()

# Onion decrypt provided ciphertext
# See the explanation for the ecnryption
def onion_decrypt_message(cip, servers):

    # TODO: insert your code here!
    for server in servers:
        iv = cip[:AES_IV_SIZE]
        cip = AES.new(server.shared_key, AES_MODE, iv).decrypt(cip[AES_IV_SIZE:])

    return cip.decode()


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
        pubkey = send_msg_to_server(server, 'pubkey_req')
        server.public_key = RSA.importKey(pubkey)
        shared_key = Random.new().read(AES_KEY_SIZE)
        server.shared_key = shared_key
        key = rsa_encrypt(shared_key, server.public_key)
        send_msg_to_server_async(server, 'shared_key '+ binascii.hexlify(key).decode())

    # Generate and onion-encrypt messages
    messages = generate_chat_messages(num_messages)
    messages_enc = []
    for m in messages:
        messages_enc.append(onion_encrypt_message(m, servers))

    # Send onion-encrypted messages to the primary server
    # See server_skeleton script for the expected format of a messsage
    # TODO: insert your code here!
    primary_server = [server for server in servers if server.server_id == PRIMARY_SERVER_ID][0]
    for message_enc in messages_enc:
        send_msg_to_server_async(primary_server, 'chat_msg_client ' + message_enc)
    return messages
# Client which is responsible for making the PIR
# It should generate appropriate random masks for each server,
# send the pir requests and finally recover the target message
# Target message is the one with the provided target_msg_index
def client_receiver(servers, num_messages, target_msg_index):

    # TODO: insert your code here!
    masks = []
    final_mask_str = ['0' for i in range(num_messages)]
    final_mask_str[target_msg_index] = '1'
    final_mask = "".join(final_mask_str)[::-1]
    final_mask = int(final_mask, 2)

    # Logic Description
    # xored = ((final_mask ^ m1) ^ m2) ^ m3
    #
    # and back
    # final_mask = ((xored ^ m3) ^ m2) ^ m1

    bitmasks = []
    for i in range(len(servers)-1):
        mask_str = [str(random.randint(0,1)) for i in range(num_messages)]
        random_mask = int("".join(mask_str), 2)
        bitmasks.append(random_mask)

    previous_mask = final_mask
    for bitmask in bitmasks:
        previous_mask = previous_mask ^ bitmask
    bitmasks.append(previous_mask)

    responses = []
    for server, bitmask in zip(servers, bitmasks):
        response = send_msg_to_server(server, 'pir_req '+ str(bitmask))
        # responses.append(response)
        responses.append(response)

    # Return the target message (string), only the body of the message,
    # without the message index
    # print(responses)
    result = responses[0]
    for r in responses[1:]:
        result = bytes_xor(result, r)
    print(result)
    return result.decode()


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
    print(target)
    print(res)
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
    # test_function()
