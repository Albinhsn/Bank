class account:

    def __init__(self, account_nmbr,  account_type, balance ):
           self.balance = balance
           self.account_type = account_type
           self.account_nmbr = account_nmbr
           
    def add_money(self, amount):
        self.balance += amount
    def remove_money(self,amount):
        self.balance -= amount
    def get_account_nmbr(self):
        return self.account_nmbr
    def show_account_info(self):
        print(f"{self.account_type}:{self.account_nmbr} - {self.ba}")
    