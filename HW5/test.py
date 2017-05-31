import hashlib
import os

while True:
    r = os.urandom(32)
    h = hashlib.sha256(r).digest()
    zeros = '\x00\x00\x00'
    if (h[0:3] == zeros) or (h[::-1][0:3] == zeros):
        print('found')
        break