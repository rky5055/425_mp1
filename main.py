import socket
import json
import logging
import sys
import os
import threading
import time
from config import *
from multicast import *
from transaction import *
from json import JSONDecodeError
from threading import Thread

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

Senders={}

class WaitGroup():
    def __init__(self):
        self.counter=0
        self.lock=threading.Lock()
        self.wait=threading.Condition()
    
    def Add(self,delta):
        with self.lock:
            self.counter+=delta
        
    def Done(self):
        self.Add(-1)

    def Wait(self):
        while True:
            counter=0
            with self.lock:
                counter=self.counter
            if counter==0:
                # logging.info("Connect success")
                return
            time.sleep(2)

SyncWaitGroup=WaitGroup()
NodeTransaction=Transaction()

def startServer(node_id, addr, port):
    global server_s
    server_s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_s.bind((addr, port))
        server_s.listen()
        logging.info(f"Server start to listen on port %d", port)
    except:
        logging.error(f"Server fail to listen" )
        return
    runServer()

def runServer():
    while True:
        try:
            client_socket, clientAddr=server_s.accept()
        except:
            logging.error("Fail to accept")
            return    
        #logging.info(f"Server successfully accept from address %s", clientAddr)
        thread=Thread(target=msg_handle, args=(client_socket, clientAddr))
        thread.setDaemon(True)
        thread.start()
    
def msg_handle(conn,clientAddr):
    f = conn.makefile()
    with conn:
        SyncWaitGroup.Wait()
        while True:
            try:
                line = f.readline()
                payload = json.loads(line)
                if payload["Type"]=="DEPOSIT":
                    NodeTransaction.Deposit(payload["To Account"], payload["Amount"])
                elif payload["Type"]=="TRANSFER":
                    NodeTransaction.Transfer(payload["From Account"], payload["To Account"], payload["Amount"])
                print(NodeTransaction.balance)
            except JSONDecodeError as err:
                logging.error("invalid request")
                continue
    
# def remove_client(client_id):
#     client=conn_group[client_id]
#     if client:
#         client.close()
#         conn_group.pop(client_id)
#         logging.info(f"Client %s disconnected", client_id)

def MakeGroup(node_id, port, config_path):
    nodesConfig=ConfigParser(config_path)
    members=[]
    for configItem in nodesConfig:
        addr=configItem.NodeHost
        post=configItem.NodePort
        members.append(Node(configItem.NodeID, addr,post))
    addr="0.0.0.0"
    members.append(Node(node_id, addr, port))
    group=NodeGroup(node_id, addr, port, members)
    return group

def startClients(group:NodeGroup):
    for node in group.members:
        startClient(group.selfNodeId, node.node_id, node.addr, node.port)

def startClient(src, dst, host, port):
    client=Client(src, dst, host, port)
    SyncWaitGroup.Done()
    Senders[client]=client

class Client:
    def __init__(self, src, dst, host, port):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect(("127.0.0.1",port))
            except Exception:
                logging.info("reconnect")
                time.sleep(5)
                continue
            break
        # logging.info(s.recv(buffersize).decode(encoding='utf8'))
        self.client=s
    
    def Send(self, msg):
        self.client.sendall(json.dumps(msg).encode('utf8'))
        self.client.sendall(b"\n")

    def Close(self):
        self.client.close()

def readinput():
    i=0
    for line in sys.stdin:
        msg=eventParser(line)
        yield msg

def Bmulticast(msg):
     for dstID, sender in Senders.items():
            sender.Send(msg)

def main():
    node_id=sys.argv[1]
    port=int(sys.argv[2])
    config_path=sys.argv[3]
    group=MakeGroup(node_id, port, config_path)
    SyncWaitGroup.Add(len(group.members))
    threading.Thread(target=startServer,args=(group.selfNodeId, group.selfNodeAddr, group.selfNodePort), daemon=True).start()
    startClients(group)
    for msg in readinput():
        Bmulticast(msg)


if __name__=="__main__":
    # node_id=sys.argv[1]
    # port=int(sys.argv[2])
    # config_path=sys.argv[3]
    main()


