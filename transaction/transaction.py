import threading
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

class Transaction:
    def __init__(self):
        self.balance={}
        self.balanceLock=threading.Lock()
    
    def Deposit(self, account, amount):
        with self.balanceLock:
            if amount<0:
                logging.error("Invalid amount")
                return 
            try:
                prevBalance=self.balance[account]
            except:
                logging.info(f"Account %s does not exist, create a new one with balance %d", account, amount)
                self.balance[account]=amount
                return
            logging.info(f"Successfully add amount %d to account %s", amount, account)
            self.balance[account]=prevBalance+amount
            return
    
    def Transfer(self, acc_from, acc_to, amount):
        with self.balanceLock:
            if amount<0:
                logging.error("Invalid amount")
                return 
            try:
                prevBalance_from=self.balance[acc_from]
            except:
                logging.error(f"Transaction fail, account %s does not exist", acc_from)
                return 
            if self.balance[acc_from]<amount:
                logging.error(f"Transaction fail, account %s does not have enough deposit", acc_from)
                return 
            self.balance[acc_from]-=amount
            try:
                prevBalance_to=self.balance[acc_to]
            except:
                logging.info(f"Account %s does not exist, create a new one with balance %d", acc_to, amount)
                logging.info("Transaction success")
                self.balance[acc_to]=amount
                return 
            logging.info("Transaction success")
            self.balance[acc_to]+=amount
            return
    


