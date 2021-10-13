import socket
import json
import sys,os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

buffersize=1024

def newClient(node_id, host, port):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    logging.info(s.recv(buffersize).decode(encoding='utf8'))
    sendHi(s,node_id)
    sendTransactionMsg(s,node_id)
    # for i in range(5):
    #     msg={"Node_id":node_id, "count":i}
    #     s.send(json.dumps(msg).encode())
    #     s.send(b'\n')
    s.close()

def sendHi(client_socket,node_id):
    jsonmsg={"Node_id":node_id, "Message": "Hi"}
    client_socket.sendall(json.dumps(jsonmsg).encode('utf8'))

def sendTransactionMsg(client_socket,node_id):
    pass

# if __name__=="__main__":

#     newClient("Node2","Server1","localhost",8001)
