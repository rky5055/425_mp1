from logging import Logger
import socket
import logging
import sys
import os
import json

class TCPClient:
    def __init__(self,srcID, dstID, addr, connection):
        self.srcID=srcID
        self.dstID=dstID
        self.addr=addr
        self.connection=connection
    def sendMsg(self,msg):
        pass


def newClient(id_src, id_dst, addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        logging.info(f"Node %s success connect to the server %s in %s",id_src, id_dst, addr)
        hi_msg={"srcid": id_src}
        s.send(json.dumps(hi_msg).encode())
        s.send(b"\n")
        return TCPClient(id_src, id_dst, addr, s)



