from cothority import Cothority
import binascii
import base64
import hashlib
import os
from operator import itemgetter
from collections import OrderedDict


# returns a list of all blocks that are stored in the skipchain # identified by the genesis-string.
# Input:
# - url where to contact the skipchain
# - genesis-block (in binary format)
# Output:
# - all blocks since the genesis-block
# Error: websockets.exceptions.ConnectionClosed indicates that # something went wrong. The error-message has more information. 
### cothority.Cothority.getBlocks(url, genesis)

# Asks the skipchain to add a block
# Input:
# - url where to contact the skipchain
# - block to store on the skipchain
# Output:
# - previous block of the blockchain
# - latest block of the blockchain which should be yours
# Error: websockets.exceptions.ConnectionClosed indicates that # something went wrong. The error-message has more information. 

### cothority.Cothority.storeBlock(url, block)

# returns a new block that appends to the last block # Input:
# - last valid block from the blockchain
# - data that will be stored in the new block. 
### cothority.Cothority.createNextBlock(last, data)


url = "ws://com402.epfl.ch:7003"
genesis = "a902de6ecd1a61cd8d7a456e18406e559898e530524ed2ba1422077a9d705c21".encode('utf-8')

genesis = binascii.unhexlify(genesis)
# genesis = base64.b64encode(b'a902de6ecd1a61cd8d7a456e18406e559898e530524ed2ba1422077a9d705c21')
# nonce = data[0:32]
# hash_of_last_block = data[32:64]
# full_email = data[64:]
print(genesis)
latest_blocks = Cothority.getBlocks(url, genesis)

latest_block = latest_blocks[-1]

lb_hash = latest_block['Hash']


leading_zeros = '\x00\x00\x00'

while True:                                
    ...:     dig = hashlib.sha256(os.urandom(32)).digest()
    ...:     print(dig[0:10])
    ...:     break
    ...:     if dig[0:12] == '\x00\x00\x00\x00':
    ...:         print('found')
    ...:         break

print(lb)