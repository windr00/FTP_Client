#encoding:utf-8
from socket import *
import sys
import os

host=raw_input('host:')
port=input('port:')
user=raw_input('your username:')
passwd=raw_input('your password:')

def login(host,port,user,passwd,s):
    s.connect((host,port))
    print "connect successfully!"
    recv=s.recv(1024)
    print recv
    s.send('TYPE I\n')
    re=s.recv(1024)
    if re[0:3]=='200':
        print 'you can use binary to transport'
    else:
        s.close()
    packetu="USER "+user+'\n'  #send someone message to server
    s.send(packetu)
    packetreu=s.recv(1024)
    print packetreu
    packetp='PASS '+passwd+'\n'  #send someone message to server
    s.send(packetp)
    packetrep=s.recv(1024)    
    print packetrep
    if packetreu[0:3]=="331"and packetrep[0:3]=="230":
        print 'thank you '+user
        return s
    else:
        print 'sorry you cannot access'
        s.close()
        
def logout(s):
    s.send('QUIT \n')
    re=s.recv(1024)
    if re[0:3]=='221':
        s.close()
        print 'already closed'
    else:
        print 'it is illegal'
    
   
def cwd(s,path):
    s.send('CWD '+path.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
    re=s.recv(1024)
    if re[0:3]=='250':
        print 'you are in:'+path
    else:
        print 'it is illegal'

def  goback(s):
    s.send('CDUP \n'.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8"))
    re=s.recv(1024)
    if re[0:3]=='250':
        print pwd(s)
    else:
        print 'it is illegal'
        
def pwd(s):
    s.send('PWD \n'.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8"))
    re=s.recv(1024)
    if re[0:3]=='257':
        print re[25:-1].decode('utf-8')
    else:
        print 'it is illegal'       
    
def dir(s):   #!!!!!!!!!
    s.send('PASV \n')
    re=s.recv(1024)
    if re[0:3]=='227':
        s.send('LIST \n')
        re1=s.recv(1024)
        if re1[0:3]=='150':
            i=0
            n=0
            while re[i]!='\n':
                if re[i]=='(':
                    i=i+1
                    tr=[]
                    j=i
                    while True:
                        if re[j]==',' or re[j]==')':
                            tr.insert(n,re[i:j])
                            i=j+1
                            n=n+1
                            if n>5:
                                break    
                        j=j+1
                if re[i-1]==')':
                    break
                i=i+1
            portf=int (tr[4])
            portl=int (tr[5])
            port=portf*256+portl
            s1=socket(AF_INET, SOCK_STREAM)
            s1.connect((tr[0]+'.'+tr[1]+'.'+tr[2]+'.'+tr[3],port))    
            while True:
                buf = s1.recv(1024)
                if not len(buf):
                    break
                print buf.decode('utf-8')
            re2=s.recv(1024)
            if re2[0:3]=='226':
                print 'close the connect in file trans port'
            else:
                print 'wait......'
        else:
            print 'it is illegal'
    else:
        print 'it is illegal'    


        
def showos(s):
    os=['windows','linux','unix']
    s.send('SYST \n')
    re=s.recv(1024)
    re=re.lower()
    if re[0:3]=='215':
        if os[0] in re:
            print 'the os is:'+os[0]
        elif os[1] in re:
            print 'the os is:'+os[1]
        elif os[2] in re:
            print 'the os is:'+os[2]
        else:
            print 'it is illegal'

def showcmd(s):
    cmds=['cmd','showos','showcmd','dir','goback','cwd', 'logout','opts','mkd','rmd','delf','changename','filesize','getfile','sendfile','pwd']         #未完                                                                                                                                 
    for cmd in cmds:
            print cmd+'_'
            
def opts(s):    #设置服务器传输所用字符集
    s.send("OPTS set utf8 on \n")
    re=s.recv(1024)
    if re[0:3]=='200':
        print 'we us UTF8 to tans'
    else:
        print 'it is illegal'

def mkd(s):# product a new directory
    dirname=raw_input('new file name is:')
    s.send('MKD '+dirname.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
    re=s.recv(1024)
    if re[0:3]=='250':
        print 'product a new directory:'+dirname
    else:
        print 'it is illegal or no such directory'
         
def rmd(s):
    delname=raw_input("delete the directory's name:")
    s.send('RMD '+delname.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
    re=s.recv(1024)
    if re[0:3]=='250':
        print 'delete the directory:'+delname
    else:
        print 'it is illegal or no such file'
         
def  delf(s):#delete file
    delname=raw_input('which file do you want to delete:')
    s.send('DELE '+delname.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
    re=s.recv(1024)
    if re[0:3]=='250':
        print 'delete the file:'+delname
    else:
        print 'it is illegal or no such file'
        
def changename(s):
    oname=raw_input('the old name is:')
    nname=raw_input('the new name is:')
    s.send('RNFR '+oname.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
    re1=s.recv(1024)
    if re1[0:3]=='350':
        s.send('RNTO '+nname.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
        re2=s.recv(1024)
        if re2[0:3]=='250':
            print 'your changing name operation is successful'
        else:
            print 'it is illegal'
    else:
        print 'it is illegal or no such file'
        
def filesize(s):
    fname=raw_input("which file's size you want:")
    s.send('SIZE '+fname.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
    re=s.recv(1024)
    if re[0:3]=='213':
        print 'the file '+fname+' size is '+re[4:]
    else:
        print 'it is illegal or no such file'
    
def getfile(s):
    filename=raw_input('which file do you want:')
    s.send('pasv \n')
    re=s.recv(1024)
    if re[0:3]=='227':
        s.send('RETR '+filename.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8")+'\n')
        re1=s.recv(1024)
        if re1[0:3]=='150':
            i=0
            n=0
            while re[i]!='\n':
                if re[i]=='(':
                    i=i+1
                    tr=[]
                    j=i
                    while True:
                        if re[j]==',' or re[j]==')':
                            tr.insert(n,re[i:j])
                            i=j+1
                            n=n+1
                            if n>5:
                                break    
                        j=j+1
                if re[i-1]==')':
                    break
                i=i+1
            portf=int (tr[4])
            portl=int (tr[5])
            port=portf*256+portl
            s1=socket(AF_INET, SOCK_STREAM)
            s1.connect((tr[0]+'.'+tr[1]+'.'+tr[2]+'.'+tr[3],port))
            try:
                f = open(filename, 'wb') 
            except:
                print 'no such file'
            while True: 
                data = s1.recv(65536) 
                if not data: 
                    print "recv file success!"
                    break
                f.write(data) 
            f.close()
            re2=s.recv(1024)
            if re2[0:3]=='226':
                print 'close the connect in file trans port'
            else:
                print 'wait......'
    else:
        print 'it is illegal'
        
        
def sendfile(s):
    try:
        path=raw_input('which is your path:')
        os.chdir(path)                                                               #change your now directory
    except:
        print 'the path is wrong'
        filename=raw_input('which file do you want:')
        s.send('pasv \n')
        re=s.recv(1024)
        if re[0:3]=='227':
            var = 'STOR '+filename+'\n'
            s.send(var.decode(sys.stdin.encoding or locale.getpreferredencoding(True)).encode("utf-8"))
            re1=s.recv(1024)
            if re1[0:3]=='150':
                i=0
                n=0
                while re[i]!='\n':
                    if re[i]=='(':
                        i=i+1
                        tr=[]
                        j=i
                        while True:
                            if re[j]==',' or re[j]==')':
                                tr.insert(n,re[i:j])
                                i=j+1
                                n=n+1
                                if n>5:
                                    break    
                            j=j+1
                    if re[i-1]==')':
                        break
                    i=i+1
                portf=int (tr[4])
                portl=int (tr[5])
                port=portf*256+portl
                s1=socket(AF_INET, SOCK_STREAM)
                s1.connect((tr[0]+'.'+tr[1]+'.'+tr[2]+'.'+tr[3],port)) 
                try:
                    f = open(filename, 'rb') 
                except:
                    print 'no such file'
                while True: 
                    data = f.read(65536) 
                    if not data: 
                        s1.close()
                        break
                    s1.send(data) 
                f.close() 
                re2=s.recv(1024)
                if re2[0:3]=='226':
                        print 'close the connect in file trans port'
                else:
                        print 'wait......'    
        else:
            print 'it is illegal'
        
    

if __name__ == "__main__":
    s=socket(AF_INET, SOCK_STREAM)
    login(host, port, user, passwd,s)
    while True:
        cmd=raw_input('what is your command:')
        if  cmd=='logout':
            logout(s)
            exit()
        elif cmd=='cwd':
            path=raw_input('your path:')
            cwd(s,path)
        elif cmd=='goback':
            goback(s)
        elif cmd=='dir':
            dir(s)
        elif cmd=='showos':
            showos(s)
        elif cmd=='showcmd':
            showcmd(s)
        elif cmd=='pwd':
            pwd(s)
        elif cmd=='opts':
            opts(s)
        elif cmd=='mkd':
            mkd(s)
        elif cmd=='rmd':
            rmd(s)
        elif cmd=='delf':
            delf(s)
        elif cmd=='changename':
            changename(s)
        elif cmd=='filesize':
            filesize(s)
        elif cmd=='getfile':
            getfile(s)
        elif cmd=='sendfile':
            sendfile(s)
        else:
            print 'no such command or it is a illegal operation'
     
    
