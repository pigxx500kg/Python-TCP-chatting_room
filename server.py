import socket
import threading

con = threading.Condition()  # 判断条件、 锁
host = input("Input the server ip address:")
port = 8888
data = ""  # 文本内容

s = socket.socket()  # 服务器套接字
print("-----------Socket created-----------")
s.bind((host, port))  # 绑定
s.listen(5)  # 监听连接 并不是最大连接数 是满后的挂起数

print("----------socket listening----------")


def NotifyAll(m):
    global data  # 全局变量
    if con.acquire():  # 获取锁 避免同时发消息造成混乱
        data = m
        con.notifyAll()  # 线程放弃占有资源的，通知其他线程从wait到执行
        con.release()  # 释放锁


def ThreadOut(conn, nick):  # 发送消息
    global data  # 全局变量
    while True:
        if con.acquire():
            con.wait()  # 堵塞，放弃对资源的占有，等消息通知
            if data:
                try:
                    conn.send(data.encode("utf-8"))  # 发送
                    con.release()
                except:
                    con.release()
                    return


def ThreadIn(conn, nick):  # 接收消息
    while True:
        try:
            temp = conn.recv(1024).decode("utf-8")
            if not temp:
                conn.close()
                return
            NotifyAll(temp)
            print(data)
        except:
            NotifyAll("-------["+nick + "] has left the room!-------")
            print(data)
            return


while True:  # 要监听多用户
    conn, addr = s.accept()  # 接受到了
    print("Connected with\tip:[{}]\tport:[{}]".format( addr[0],str(addr[1])))
    nick = conn.recv(1024) # 接受昵称
    nick = nick.decode("utf-8")
    NotifyAll("------Welcome" + " [" + nick + "] " + "to the room!------")#.encode("utf-8")
    print(data)
    conn.send(data.encode("utf-8"))
    threading.Thread(target=ThreadOut, args=(conn, nick)).start()
    threading.Thread(target=ThreadIn, args=(conn, nick)).start()
