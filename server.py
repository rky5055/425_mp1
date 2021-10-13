import socket
import logging
import json
import threading

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

buffersize=1024
port=8001
def startServer(nodeID, addr, port):
    server_s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_s.bind(("", port))
        server_s.listen()
    except:
        logging.error(f"Node %s fail to listen", nodeID)
        return
    logging.info("Server start to listen")
    return server_s

def runServer(waitGroup, nodeID, socket, router):
    with socket as s:
        try:
            connection,_=s.accept()
        except:
            logging.error(f"Node %s fail to accept", nodeID)
        handleConn(waitGroup, nodeID, connection, router)

def handleConn(waitGroup, nodeID, connection, router):
    with connection as conn:
        data, _=conn.recv()
        data.split()








