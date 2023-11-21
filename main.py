import os
import count
import draw
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA
from Cryptodome.Signature import PKCS1_v1_5
import datetime
import RED


def send_cands():
    f=open('cands','r')
    cands = f.read();f.close()
    cands= cands.replace('_',' ')
    if check_cands():
        return cands

def check_cands():
    pub=RSA.import_key(open ('cand_pub_key','rb').read())
    signature = PKCS1_v1_5.new(pub)
    proof=open('cand-hash','rb').read()
    cands = open('cands').read()
    if signature.verify(SHA.new(cands.encode('utf-8')),proof):
        return True
    else:
        return False
    

def check_voter(nick:str):#checks the confirmation of vote
    pub=RSA.import_key(open ('keys/'+nick,'rb').read())
    signature = PKCS1_v1_5.new(pub)
    proof=open('hashes/'+nick,'rb').read()
    candid = open('votes/'+nick).read()
    if signature.verify(SHA.new(candid.encode('utf-8')),proof):
        return True
    else:
        return False


def send_welcome(message):
    return ("Здравствуйте, я бот для того, чтобы голосовать за кандидата")


def extract_arg(arg:str):
    return arg.split()[1:]
    

def regist(id:str,nick:str):
    nicks=open('nicks','r').read().split()
    ids=open('ids','r').read().split()
    
    if id not in ids:
        if nick not in nicks:
            nicks.append(nick)
            ids.append(id)

            priv = RSA.generate(2048)#encrypting
            pub = priv.publickey()
            shifr = PKCS1_OAEP.new(pub)
            nick = nick.encode("utf-8")
            pas = shifr.encrypt(nick)

            f=open('nicks-encr/'+nick.decode("utf-8"),'wb')
            f.write(pas)
            f.close()

            f=open('nicks','a')
            f.write(nicks[len(nicks)-1]+'\n')
            f.close()

            f=open('ids','a')
            f.write(id+'\n')
            f.close()

            f=open('keys/'+nick.decode("utf-8"),'wb')
            f.write(bytes(pub.exportKey('PEM')))
            f.close()

            f=open('privs/'+nick.decode("utf-8"),'wb')
            f.write(bytes(priv.exportKey('PEM')))
            f.close()
            return 'Вы зарегистрировали на себя аккаунт для голосваний с ником '+nick.decode('utf-8')
        else:
            return 'Простите, но этот ник уже задействован'
    else:
        return 'Простите, но у вас уже есть ник'






def results():
    print ('start viewing')
    ans=''
    for i in range (len (count.arrcount(sear='names'))):
        reso = count.arrcount(sear='scores')[i]
        summ = count.summ()
        reso = round (reso*100/summ)

        ans = ans+count.arrcount(sear='names')[i] +'      '+str(reso)+'%\n'
    if count.summ()>0:
        #draw.drawed()
        return ans
    else:
        ans = 'Никто ещё не проголосовал'    
        return ans
    
def voters():
    ans = ''
    nicks=open('nicks').read().split()
    for i in range(len(nicks)):
        try:
            nick=nicks[i]
            vot=open('votes/'+nick).read()
            if check_voter(nick):
                print('checked voter')
                ans+=nick+'  '+vot+'\n'
            else:
                ans+=nick+'  __None__\n'
        except:
            ans+=nick+'  __None__\n'
    r=open('report','w')
    r.write(ans)
    r.close()

def get_id(nick:str):
    nicks=open('nicks').read().split()
    num=nicks.index(nick)
    ids=open('ids').read().split()
    return ids[num]




def vote(cap:str,file):

    
    now=datetime.datetime.now()
    if now.hour >= 7 and now.hour<21 or True:
        args = cap.split()
        if args [0] == '!vote':
            nick = args[1]
            #priv = RSA.import_key(open ('','rb').read())#bytes (args[1], 'utf-32')

            candid = str(args[2])#for whom is voted

            #get the candidat`s name from his number


            

            cn=open('cands','r');cands=cn.read();cn.close()
            cands=cands.split()
            

            candid=cands[int(candid)]
            candid=candid[candid.index('.')+1:candid.index(':')]

            ncands=['']*len(cands)
            for i in range(len(cands)):
                string=cands[i]
                ncands[i]=string[string.index('.')+1:string.index(':')]

            try:
                proofcand = open('cand-hash','rb').read()
            except:
                RED.terminate()
                return'red alert'
            print('hash opened')

            
            if candid in ncands and check_cands():
                f=open('nicks','rb')#open file with nickes of all electorat
                nicksfl=f.read()
                nicksfl = nicksfl.split()[0:]#this an array
                nick = nick.encode('utf-8')
                

                if (nick in nicksfl):#does this nick exists

                    for i in range (len(nicksfl)):#here we get the number of user
                        if nick == nicksfl[i]:
                            num = i
                    


                


                priv = RSA.import_key(file)
                shifr=PKCS1_OAEP.new(priv)

                ps = open('nicks-encr/'+str(nick.decode('utf-8')), 'rb')
                ecr = ps.read()



                if str(shifr.decrypt(ecr)) == str(nick):#if the private key was right

                    sig = PKCS1_v1_5.new(priv)
                    hashed = SHA.new(candid.encode('utf-8'))
                    enccandid=sig.sign(hashed)
                    v=open('votes/'+nick.decode('utf-8'),'w')
                    v.write(candid)
                    v.close()
                    vhsh = open('hashes/'+nick.decode('utf-8'), 'wb')
                    vhsh.write(enccandid)
                    vhsh.close()
                    
                    l=open ('logs','a')

                    now = datetime.datetime.now()
            
                    dt_string = now.strftime("%d/%m/%Y-%H:%M:%S")
                    l.write ('b^'+nick.decode('utf-8')+ '_' + candid + '!' +dt_string+'\n')      #write vote to logs
                    l.close()
                    #draw.drawed()
                    return 'Ваш голос за кандидата ' + candid +' засчитан, пользователь '+nick.decode('utf-8')+'.'
            elif not check_cands() and candid in ncands:
                RED.terminate()
                return'red alert'
            elif not candid in ncands:
                return 'Мы не знаем такого кандидата. Попробуйте /cands чтобы увидеть всех кандитатов'
        else:
            return 'Ошибка. Начните команду с !vote'
    else:
        return'Простите, но время голосования вышло'





