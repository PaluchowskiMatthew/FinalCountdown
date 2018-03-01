#!/usr/bin/env python

import asyncio
import websockets
import hashlib
import binascii
import random

def enc(number):
    buff = number.to_bytes((number.bit_length() + 7) // 8, 'big')
    return binascii.hexlify(buff).decode()
    
def dec(msgReceived):
    buff = binascii.unhexlify(msgReceived)
    return int.from_bytes(buff, 'big')

def int_to_bytes(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big')

def int_to_hex(number):
    return format(number, 'x')
    
def sha(stringInput):
    return hashlib.sha256(stringInput).digest()
    #return hashlib.sha256(str(stringInput).encode('utf-8')).hexdigest()

def sha_to_int(sha):
    return int(sha, 16)
    
def sha_to_bytes(sha):
    return binascii.unhexlify(sha)

def cryptrand(n=1024):
    hex_N = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
    int_N = int(hex_N, 16)
    return random.SystemRandom().getrandbits(n) % int_N
    
async def pake():
    async with websockets.connect('ws://com402.epfl.ch/hw2/ws') as websocket:

        email = 'mateusz.paluchowski@epfl.ch'
        hex_N = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
        int_N = dec(hex_N)
        print('N: ', int_N)
        g = 2
        
        #1
        await websocket.send(email.encode('utf-8'))

        salt = await websocket.recv()
        salt_int = dec(salt)
        print('salt: ', salt)
        print('salt_int: ', salt_int)
        
        #2
        a = cryptrand(32)
        print('a: ', a)
        capital_A_int = pow(g, a, int_N)
        print('A raw: ', enc(capital_A_int))
        print('A: ', capital_A_int)
        await websocket.send(enc(capital_A_int))
        
        capital_B =  await websocket.recv()
        capital_B_int = dec(capital_B)
        print('B raw: ', capital_B)
        print('B: ', capital_B_int)
        
        
        #3
        p = 'IwQCAAdTCUseBUwUQwAaGhIFSTQKUAIDDgJI'
        A_and_B = int_to_bytes(capital_A_int) + int_to_bytes(capital_B_int)
        print('A_and_B bytes: ', A_and_B)
        print('salt raw: ', salt)
        u = sha(A_and_B)
        print('u raw: ', u)
        u = int(binascii.hexlify(u), 16)
        print('u: ', u)
        
        user_pass = email.encode('utf-8') + b':' + p.encode('utf-8')
        print("User_pass: ", user_pass)
        x2 = sha(email.encode('utf-8') + b':' + p.encode('utf-8'))
        print('x2 raw: ', x2)
        x = sha( int_to_bytes(salt_int) + x2 )  
        print('x raw: ', x)
        x = int(binascii.hexlify(x), 16)
        print('x: ', x)
        
        first = capital_B_int - pow(g, x, int_N)
        print('first: ', first)
        second = (a + ((u*x) %  int_N)) % int_N
        print('second: ', second)
        capital_S_int = pow(first, second, int_N)
        print('S: ', capital_S_int)
        
        
        token_req = hashlib.sha256( int_to_bytes(capital_A_int) + int_to_bytes(capital_B_int) + int_to_bytes(capital_S_int) ).hexdigest()
        print('token_req int: ', token_req)
        await websocket.send(token_req)
        
        token =  await websocket.recv()
        print('token: ', token)

asyncio.get_event_loop().run_until_complete(pake())