#-*- coding: utf-8 -*-
from socket import *
from time import ctime
from time import localtime
import time

HOST=''
PORT=1122  #设置侦听端口
BUFSIZ=1024
ADDR=(HOST, PORT)

# AF_INET:服务器之间网络通信 SOCK_STREAM:流式socket, for TCP
# 就是在建立一个新的socket
sock=socket(AF_INET, SOCK_STREAM)

# 将套接字绑定到地址上
sock.bind(ADDR)

# 开始监听TCP传入连接，内部数字指可挂起的最大连接数量
sock.listen(5)

#设置退出条件
STOP_CHAT=False
while not STOP_CHAT:
    print('等待接入，侦听端口:%d' % (PORT))
    # sock.accept()的作用
    # 接受TCP连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。
    tcpClientSock, addr=sock.accept()
    print('接受连接，客户端地址：',addr)
    while True:
        try:
            data=tcpClientSock.recv(BUFSIZ)
        except:
            #print(e)
            tcpClientSock.close()
            break
        if not data:
            break
        #python3使用bytes，所以要进行编码
        #s='%s发送给我的信息是:[%s] %s' %(addr[0],ctime(), data.decode('utf8'))
        #对日期进行一下格式化
        ISOTIMEFORMAT='%Y-%m-%d %X'
        stime=time.strftime(ISOTIMEFORMAT, localtime())
        s='%s发送给我的信息是:%s' %(addr[0],data.decode('utf8'))
        tcpClientSock.send(s.encode('utf8'))
        print([stime], ':', data.decode('utf8'))
        #如果输入quit(忽略大小写),则程序退出
        STOP_CHAT=(data.decode('utf8').upper()=="QUIT")
        if STOP_CHAT:
            break
tcpClientSock.close()
sock.close()