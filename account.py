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
        
#Closes account for customer after ssn and account id input
def remove_account(ssn, ds, state):
        # Requests accounts by ssn from datasource
        ds._find_accounts_by_ssn(ssn)
        if state.read():
            state.seek(0)
            acc_ids = []
            for line in state:  # Reads the requests accounts and prints them
                line = line.strip().split(':')
                print(
                    f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
                acc_ids.append(line[0])
            print("Enter id to remove 'e' to exit")
            i = input()
            if i == 'e':
                return
            if i in acc_ids:
                # Removes the account if input is valid
                ds._remove_account(i)
                return
            else:
                print("Enter a valid account id please")
        print("No accounts belonging to ssn")
        return
#Prints accounts belonging to ssn
def print_accounts(ssn, ds, state):
    ds._find_accounts_by_ssn(ssn)  # Requests accounts to state
    if state.read():
        state.seek(0)
        for line in state:
            line = line.strip().split(':')
            print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
        return
    print("No account belonging to ssn")
#Creates account based on ssn
def create_account(ssn, ds, state):
    while True:
        try:
            tpe = input("Choose account type:\n1. debit account 2. savings account 'e' to exit\n")
            # Requests valid account id to state
            ds._get_valid_id("accounts")
            acc_id = int(state.readline().strip())+1
            if tpe == '1' or tpe == '2':
                if tpe == '1':
                    tpe = "debit account"
                else:
                    tpe = "savings account"
                # Sends request to open account
                ds._open_account(account(acc_id, tpe, 0), ssn)
                print(f"Account added with account number: {acc_id}")
                return
            elif tpe == 'e':
                return
            else:
                print("Enter valid input")
        except:
            print("Enter valid input")
