class account:

    def __init__(self, id, tpe, balance):
           self.balance = balance
           self.tpe = tpe
           self.id = id
    
    #Checks whether withdraw is possible with given amount
    def check_withdraw_eligibility(self, amount):
        if(amount<0):
            amount = amount * -1
        if self.balance >= amount:
            return 1
        print(f"Can't withdraw more then balance {self.balance}")
        return -1
    
    #Changes balance based on parameter
    def change_balance(self, amount):
        self.balance += amount
        print(f"New balance: {self.balance}")