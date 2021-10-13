import socket
import logging
import json
from threading import Thread
import time

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

buffersize=1024
counter=0
conn_group={}
server_s=None

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
    thread=Thread(target=runServer)
    thread.setDaemon(True)
    thread.start()

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
    

def msg_handle(client_socket,clientAddr):
    client_id=""
    client_socket.sendall("Connect server successfully".encode(encoding='utf8'))
    SyncWaitGroup.Wait()
    while True:
        try:
            bytemsg=client_socket.recv(buffersize)
            data=json.loads(bytemsg.decode(encoding='utf8'))
            client_id=data["Node_id"]
            client_msg=data["Message"]
            if client_msg=="Hi":
                # global counter
                # counter+=1
                conn_group[client_id]=client_socket
                logging.info(f"Server receives Hi from Node %s", client_id)
            else:
                logging.info(f"Server receives Transaction msg from Node %s", client_id)
        except:
            remove_client(client_id)
            break
    
def remove_client(client_id):
    client=conn_group[client_id]
    if client:
        client.close()
        conn_group.pop(client_id)
        logging.info(f"Client %s disconnected", client_id)

# if __name__=="__main__":
#     startServer()
#     thread=Thread(target=runServer)
#     thread.setDaemon(True)
#     thread.start()

#     while True:
#         time.sleep(0.1)