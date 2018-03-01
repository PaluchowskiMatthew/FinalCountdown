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
genesis = binascii.unhexlify("a902de6ecd1a61cd8d7a456e18406e559898e530524ed2ba1422077a9d705c21")
full_email = "mateusz.paluchowski@epfl.ch".encode()
    
latest_block = Cothority.getBlocks(url, genesis)[-1]

blocks_accepted = []
blocks_rejected = []
while True:
    nonce = os.urandom(32)
    hash_of_last_block = latest_block.Hash
    
    data = nonce + hash_of_last_block + full_email
    hash_hexdigest = hashlib.sha256(data).hexdigest()
    
    if hash_hexdigest.startswith('00000'):
        new_block = Cothority.createNextBlock(latest_block, data)
        
        try:
            previous, current_latest_block = Cothority.storeBlock(url, new_block)
            if (current_latest_block == new_block):
                blocks_accepted += [new_block]
            else:
                blocks_rejected += [new_block]
            latest_block = current_latest_block
            print(latest_block)
        except e:
            print(e)
    
    if len(blocks_accepted) >= 5:
        break