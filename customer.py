from lib2to3.pytree import Base
from transaction import transaction
from account import account
class customer:
    
    def __init__(self, nm, ssn):
        self.name = nm
        self.ssn = ssn #Social security number

#Prints every customer
def print_customers(ds, state):
    ds.get_all()  # Requests all customers from datasource
    for line in state:
        line = line.strip().split(':')
        a = ""
        #3 first lines in line is id,name,ssn and the rest is account info of length 3
        for l in range((len(line)-1)//3):
            a += f"\n       {line[l*3+2]}       {line[l*3+3]}       {line[l*3+4]} "
        print(f"Name: {line[0]}   ssn:{line[1]}\n     Account id    Account type       Balance{a}")

#Deposits after inpput of ssn and acc id
def deposit(ssn, ds, state):
    # Sends requests for accounts with assigned ssn
    ds.find_accounts_by_ssn(ssn)
    if state.read():
        state.seek(0)
        accounts = []
        for line in state:  # Reads through state and adds id's and creates account objects and prints them
            line = line.strip().split(':')
            print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
            accounts.append(
                account(int(line[0]), line[1], float(line[2])))
        i = input("Enter id to Deposit to  'e' to exit\n")
        if i == 'e':
            return
        for a in accounts:
            if int(i) == a.id:  # Checks if input is valid
                while True:
                    amount = input(
                        "Enter amount to deposit 'e' to exit\n")
                    if amount == 'e':
                        return
                    try:
                        amount = float(amount)
                        # Creates a transaction for account with given amount
                        a.change_balance(amount)
                        # Sends update request to datasource
                        ds.update_account(a)
                        transaction(a.id, amount, ds)
                        return
                    except:
                        print("Enter valid amount please")
        print("Enter a valid account id please")
    print("No accounts belonging to ssn")
    return  # No accounts belonged to valid ssn so returning to menu

#Withdraw after inpput of ssn and acc id
def withdraw(ssn, ds, state):
    # finds accounts with ssn and writes to state
    ds.find_accounts_by_ssn(ssn)
    if state.read():  # Checks whether or not accounts exists with given input
        while True:
            state.seek(0)
            accounts = []
            for line in state:
                line = line.strip().split(':')
                print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
                accounts.append(account(int(line[0]), line[1], float(line[2])))
            print("Enter id to Withdraw from 'e' to exit")
            i = input()
            if i == 'e':
                return
            for a in accounts:
                if int(i) == a.id:
                    while True:
                        print("Enter amount to Withdraw 'e' to exit")
                        try:
                            amount = input()
                            if amount == 'e':
                                return
                            amount = -float(amount)
                            # Check whether withdraw amount exceeds balance
                            if a.check_withdraw_eligibility(amount) != -1:
                                # Changes balance with given amount
                                a.change_balance(amount)
                                # Sends update request for account
                                ds.update_account(a)
                                # Creates a transaction
                                transaction(a.id, amount, ds)
                                return
                        except:
                            print("Enter valid amount please")
            print("Enter a valid account id please")
    print("No accounts belonging to ssn")
    return  # No accounts belonged to valid ssn so returning to menu

#Removes customer after ssn as input
def remove_customer(ssn, ds):
    try:
        ssn = int(ssn)
        # This function can break with wrong input
        ds.remove_customer_by_ssn(ssn)
        return
    #Handles exception if ssn input is invalid
    except:
        print("SSN didn't exist, check if valid format")

#Prints customer info by ssn
def get_customer(ssn, ds, state):
        ds.find_customer_by_ssn(ssn)
        if state.read():  # Checks if customer exists
            state.seek(0)
            line = state.readline().strip().replace('#', '').split(":")
            print(f"Name: {line[0]}   ssn:{line[1]}")
            return
        else:
            print("No customer with that ssn")

def get_all_transactions(ssn, ds, state):
    while True:
        ds.find_accounts_by_ssn(ssn)
        a = []
        for line in state:
            line = line.strip().split(':')
            print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
            a.append(line[0])
        print("Enter id to print transactions 'e' to exit")
        i = input()
        if i == 'e':
            return
        elif i in a:
            ds.find_transactions_by_id(i)
            print(f"Account: {i}")
            state.seek(0)
            for line in state:
                line = line.strip().split(':')
                print(f"Date: {line[0]} Amount:{line[1]}")
            return
        else:
            print("Enter a valid account id please")

def change_customer_name(ds, state):
    while True:
        try:
            ssn = input("Enter ssn for customer. 'e' to exit\n")
            if ssn == 'e':
                return
            ssn = int(ssn)
            ds.find_customer_by_ssn(ssn)
            state.seek(0)
            nm, s = state.readline().strip().split(':')  # Reads id, name and ssn from state
            n = input("Enter new name\n")
            # Creates new customer object from old info and input
            ds.update_customer(customer(n, ssn))
            return
        #Handles exception if ssn is invalid
        except BaseException as e:
            print(e) 
            print("Enter a valid id")
#Creates a customer after input of name and ssn
def create_customer(ds, state):
    while True:
        n = input("Enter name\n")
        ssn = int(input("Enter ssn (12 numbers)\n"))
        if len(str(ssn)) != 12:
            print("enter valid length of ssn (12)")
            continue
        try:
            ds.create_customer(customer(n, ssn))
            break
        except:
            print("Customer already exists with ssn")
            return
    print(f"Created customer with ssn {ssn}")
