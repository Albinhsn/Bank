
from re import T
from datasource import datasource
from customer import customer
from account import account
class bank:
    
    def __init__(self):
        print("Welcome to the bank!")
        self._load()
        self.f = open('user_data.txt','r+')
        self.get_customers()
        self.getValidAccountId()
    def _load(self):
        self.ds = datasource()
        
    def get_customers(self):
        self.list_of_customers = []
        self.f.seek(0)
        for idx, line in enumerate(self.f):
            line = line.strip().replace('#',':').split(':')
            self.list_of_customers.append(customer(line[0], line[1], line[2]))
            for l in range(int((len(line)-3)/3)):
                self.list_of_customers[idx].accounts.append(account(line[3+l*3], line[4+l*3],line[5+l*3]))
        
    def add_customer(self):
        print("Enter name:")
        nm = input()
        print("Enter social security number")
        scn = input()
        id = self.getValidId()
        self.list_of_customers.append(customer(id,nm,scn))   
        
    def change_customer_name(self, id):
        print("What would you like to change your name to?")
        nme = input()
        for cstm in self.list_of_customers:
            if(id == cstm.id):
                cstm.name = nme
                return
    def getValidCustomerId(self):
        highest_id = 0
        self.f.seek(0)
        for line in self.f:
            line = line.split(":")
            if(highest_id<line[0]):
                highest_id = line[0]
        return highest_id +1
    
    def get_customer(self, id):
        for cstm in self.list_of_customers:
            if(cstm.id == id):
                cstm.printInfo()
        
        
    def remove_customer(self, id):
        for cstm in self.list_of_customers:
            if(id == cstm.id):
                for acc in cstm.accounts:
                    cstm.deleteAccount(acc.id)
                self.list_of_customers.pop(self.list_of_customers.index(cstm))
                return

    def add_account(self, scn):
        id = self.getValidAccountId()
        while True:
            try:
                print("""What type of card you want
        1. debit account
        2. savings account
                    """)
                ans = int(input())
                if(ans == 1):
                    for cstm in self.list_of_customers:
                        if(scn == cstm.scn):
                            cstm.accounts.append(account(id, 'debit account', 0))
                            return id
                elif(ans == 2):
                    for cstm in self.list_of_customers:
                        if(scn == cstm.scn):
                            cstm.accounts.append(account(id, 'debit account', 0))
                            return id
                else:
                    print("Try again please, valid input is '1' or '2'")
            except:
                print("Try again please, valid input is '1' or '2'")
    def getValidAccountId(self):
        highest_id = 0
        self.f.seek(0)
        for line in self.f:
            line = line.replace('#',':').strip().split(':')
            if(len(line)>3):
                for l in range(int((len(line)-3)/3)):
                    if(highest_id<int(line[3+l*3])):
                        highest_id = int(line[3+l*3])
        return highest_id + 1 
    def closeAccount(self, scn, id):
        for cstm in self.list_of_customers:
            if(cstm.scn == scn):
                cstm.deleteAccount(id)
        
    def get_account(self,scn, id):
        for cstm in self.list_of_customers:
            if(scn == cstm.scn):
                for acc in cstm.accounts:
                    if(acc.id == id):
                        acc.show_account_info()
                        return
        
    def deposit(self, scn, acc_id, amount):
        for cstm in self.list_of_customers:
            if(scn == cstm.scn):
                return cstm.deposit_money(acc_id, amount)
        return False
    def withdraw(self, scn, acc_id, amount):
        for cstm in self.list_of_customers:
            if(scn == cstm.scn):
                return cstm.withdraw_money(acc_id, amount)
        
    def close_account(self,scn, id):
        for cstm in self.list_of_customers:
            if(scn == cstm.scn):
                for acc in cstm.accounts:
                    if(acc.id == id):
                        print(f"Deleting account {acc.id} with balance {acc.balance}")
                        return acc.balance
    
    def get_all_transactions_by_pnr_acc_nr():
        print()
        
    def updateTxtFile():
        pass