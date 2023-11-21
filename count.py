from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA
from Cryptodome.Signature import PKCS1_v1_5


def arrcount (sear:str):

    candids = []
    results = []
    nicksfl = open ('nicks','r')
    nicksfl = nicksfl.read()
    nicksfl = nicksfl.split()
    for i in nicksfl:
        try:
            f=open('votes/'+i,'r')
            fsh=open('hashes/'+i, 'rb')
            vote = f.read();f.close()
            sigvote = fsh.read();fsh.close()
            pub = RSA.import_key(open ('keys/'+i,'rb').read())
            hsh = SHA.new(vote.encode('utf-8'))
            signature = PKCS1_v1_5.new(pub)

            if signature.verify(hsh,sigvote):
                num=0
                if vote not in candids:
                    candids.append(vote)
                    results.append (0)
                for j in range (len (candids)):
                    if candids[j] == vote:
                        num=j
                        break
                results[num]=results[num]+1
        except:
            continue
    if sear=='names':
        return candids
    elif sear == 'scores':
        return results


def summ():
    scs = arrcount(sear='scores')
    sum=0
    for i in scs:
        sum = sum + i
    return sum






        
