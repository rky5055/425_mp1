import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def eventParser(rawmsg):
    msg=rawmsg.split(" ")
    json={}
    if msg[0]=="DEPOSIT":
        try:
            accName, depositAmount=msg[1], int(msg[2])
            jsonpack={"Type":"DEPOSIT", "From Account":"None", "To Account":accName, "Amount":depositAmount}
        except:
            logging.error("Invalid DEPOSIT input format")
    elif msg[0]=="TRANSFER":
        try:
            accName_from, accName_to, transferAmount=msg[1], msg[3], int(msg[4])
            jsonpack={"Type":"TRANSFER", "From Account":accName_from, "To Account":accName_to, "Amount":transferAmount}
        except:
            logging.error("Invalid TRANSFER input format")
    else:
        logging.error("Invalid OPERATION")

    return jsonpack
