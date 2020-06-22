import socket
import threading


outString = ""
nick = ""
inString = ""


def client_send(sock):  # 通过线程调用函数
    global outString  # 定义全局变量
    flag = 0 # 退出标识
    while True:  # 可以一直发消息
        outString = input()  # 接受输入
        if outString == "exit": # 用户想退出聊天室
            flag = 1
        outString = "[" + nick + "]" + ": " + outString  # 消息格式
        sock.send(outString.encode("utf_8"))
        if flag == 1:
            sock.close()
            break



def client_accept(sock):
    global inString
    while True:
        try:
            inString = sock.recv(1024).decode("utf-8")  # 接收数据
            if not inString:
                break
            if outString != inString:  # 不把自己的信息显示出来
                print(inString)
        except:
            break


nick = input("input your nickname:")  # 输入昵称
ip = input("input the server ip address:")  # 输入ip地址
port = 8888  # 端口号
sock = socket.socket()  # 创建TCP套接字
sock.connect((ip, port))  # 连接
sock.send(nick.encode("utf-8"))  # 把名字发送给 server

'''
由于input函数的阻塞作用，以上的代码发完一条信息，只能等待另一端的信息发过来才能继续发送。 
这时就要考虑将输入与接收分开来，
将接收的函数从主线程里抓出来丢到另一个线程里单独运行，为实现这一功能，必须引入多线程。
'''
th_send = threading.Thread(target=client_send, args=(sock,))  # 发送信息的线程
th_send.start()
th_accept = threading.Thread(target=client_accept, args=(sock,))  # 接受信息的线程
th_accept.start()
