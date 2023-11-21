import os 


def terminate ():
    keys=os.listdir('keys/')
    hashes=os.listdir('hashes/')
    nicks_enc=os.listdir('nicks-encr/')
    privs=os.listdir('privs/')
    votes=os.listdir('votes/')


    f=open('nicks','w')
    f.write('')
    f.close()

    f=open('ids','w')
    f.write('')
    f.close()
    for i in keys :
        try:
            os.remove('keys/'+i)
        except:
            print()
    for i in hashes :
        try:
            os.remove('hashes/'+i)
        except:
            print()
    for i in nicks_enc :
        try:
            os.remove('nicks-encr/'+i)
        except:
            print()
    for i in privs :
        try:
            os.remove('privs/'+i)
        except:
            print()
    for i in votes :
        try:
            os.remove('votes/'+i)
        except:
            print()
    f=open('cands','w')
    f.write('')
    f.close()

    f=open('cands-hash','w')
    f.write('')
    f.close()



terminate()