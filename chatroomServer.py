import socket
from threading import Thread

clients={}
address={}

Host='127.0.0.1'
Port=8080


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((Host,Port))

def accept_client_connections():
    while True:
        client_con,client_address=s.accept()
        print(client_address," has connected")
        client_con.send("Welcome to the chat room! Who are you?".encode('utf8'))
        address[client_con]=client_address
        Thread(target=handle_client,args=(client_con,client_address)).start()

def broadcase(msg,prefix=""):
    for x in clients:
        x.send(bytes(prefix,'utf8')+msg)
    
def handle_client(conn,addr):
    name=conn.recv(1024).decode()
    welcome='Welcome '+name+' you can type #quit to quit the caht room'
    conn.send(bytes(welcome,'utf8'))
    msg=name+ ' has recently joined the chat room'
    broadcase(bytes(msg,'utf8'))
    clients[conn]=name
                    
    while True:
        msg=conn.recv(1024)
        if msg!=bytes('#quit','utf8'):
            broadcase(msg,name+':')
        else:
            conn.send(bytes('#quit','utf8'))
            conn.close()
            del clients[conn]
            broadcase(bytes(name+' has left the chatroom','utf8'))
            break
    
if __name__=='__main__':
    s.listen(5)
    print('The server is now listening to clients requests')
    t1 =Thread(target=accept_client_connections)
    t1.start()
    t1.join()