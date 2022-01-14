from account import account
class customer:
    
    def __init__(self, id, nm, scn):
        self.id = id
        self.name = nm
        self.scn = scn #Social security number
        self.accounts = []
    def printInfo(self):
        print(f"{self.id} {self.name} {self.scn}")
        for acc in self.accounts:
            acc.show_account_info()
    def deposit_money(self, acc_id, amount):
        for acc in self.accounts:
            if(acc.id == acc_id):
                acc.balance += amount
                return True
        return False 
    
    def withdraw_money(self, acc_id, amount):
        for acc in self.accounts:
            if(acc.id == acc_id):
                if(acc.balance - amount>=0):
                    acc.balance -= amount
                    return True
                else:
                    return False 
           
    def deleteAccount(self, id):
        for acc in self.accounts:
            if(id == acc.id):
                self.accounts.pop(self.accounts.index(acc))
                return
    