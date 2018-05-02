import random as rand
import hashlib


def hex_me(a):
    if a == 10:
        return 'A'
    if a == 11:
        return 'B'
    if a == 12:
        return 'C'
    if a == 13:
        return 'D'
    if a == 14:
        return 'E'
    if a == 15:
        return 'F'
    else:
        return a

#def hexrandom(minint, maxint):
#    x = str(rand.randint(int(minint), int(maxint)))

#count1, count2, count3 = 0
for a in range(0,16):
    for b in range(0,16):
        for c in range(0,16):
            for d in range(0,16):
                print str(hex_me(a))+str(hex_me(b))+str(hex_me(c))+str(hex_me(d))


