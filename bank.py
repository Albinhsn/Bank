from datasource import datasource
from customer import customer
from account import account
from transaction import transaction
class bank:  
    def __init__(self):
        print("Welcome to the bank!")
        self._load()
        self.run_system()
    #Main loop/Main Menu
    def run_system(self): 
        while True:
            inp = input("1. Print ALL customers   2. Add customer   3. Change customer name   4. Remove customer  5. Create account   6. Remove Account   7. Print transactions by account   8. Print accounts\n 9. Withdraw   10. Deposit   11. Print customer info  'E'. Exit\n")
            self.update_state()
            if(inp == '1'):
                self.print_customers()
            elif(inp == '2'):
                self.create_customer()
            elif(inp == '3'):
                self.change_customer_name()
            elif(inp == '4'):
                self.remove_customer()
            elif(inp == '5'):
                self.create_account()
            elif(inp == '6'):
                self.remove_account()
            elif(inp == '7'):
                self.get_all_transactions_by_pnr_acc_nr()
            elif inp == '8':
                self.print_accounts()
            elif inp == '9': 
                self.withdraw()
            elif(inp == '10'):
                self.deposit()
            elif(inp == '11'):
                self.get_customer()
            elif(inp == 'E'):
                print("Thanks for using the bank")
                exit()
            else:
                print("Wrong input try again")
    #Loads datasource and opens state file
    def _load(self):
        self.ds = datasource()
        self.__state = open('state.txt', 'r+')
    #Prints every customer 
    def print_customers(self):
        self.ds.get_all() #Requests all customers from datasource
        for line in self.__state: 
            line = line.strip().split(':')
            a = ""
            #3 first lines in line is id,name,ssn and the rest is account info of length 3
            for l in range((len(line)-1)//3): 
                a += f" ||  Account id:{line[l*3+3]}  Account type: {line[l*3+4]} Balance: {line[l*3+5]} "
            print(f"id: {line[0]}  Name: {line[1]}   ssn:{line[2]}   {a}")
    #Creates a customer after input of name and ssn
    def create_customer(self):
        while True:
            n = input("Enter name\n")
            try:
                ssn = int(input("Enter ssn (12 numbers)\n"))
                if len(str(ssn)) != 12:
                    print("enter valid length of ssn (12)")
                    continue        
                self.ds.get_valid_id("user")  # Requests the highest used customer id
                self.__state.seek(0)
                i = int(self.__state.readline().strip())+1
                print(i)
            except BaseException as e :
                print(e)
                print("Please enter valid ssn")
                continue
            try:
                self.ds.create_customer(customer(i, n, ssn))
                break
            except:
                print("Customer already exists with ssn")
                return
        print(f"Created customer with id {i}")       
    #Changes customer name
    def change_customer_name(self):
        while True: 
            i = input("Enter id for customer. 'e' to exit\n")
            if i == 'e':
                return
            else:
                try:
                    #This function can break with wrong input
                    self.ds.find_customer_by_id(i) #Requests customer info from datasource by id                
                    self.__state.seek(0)
                    id, nm, ssn = self.__state.readline().strip().split(':') #Reads id, name and ssn from state
                    n = input("Enter new name\n")
                    self.ds.update_customer(customer(id, n, ssn)) #Creates new customer object from old info and input
                    return
                #Handles exception if input is invalid (customer id)
                except:
                    print("Enter a valid id")       
    #Removes customer after ssn as input
    def remove_customer(self):
        while True:       
                i = input("Enter ssn you'd like to remove. 'e' to exit\n")
                if i == 'e':
                    return
                else:
                    try:    
                        i = int(i)
                        self.ds.remove_customer_by_ssn(i) #This function can break with wrong input
                        return
                    #Handles exception if ssn input is invalid
                    except:
                        print("SSN didn't exist, check if valid format")
    #Creates account for customer
    def create_account(self):
        while True:
            try:
                ssn = input("Enter ssn to create account for. 'e' to exit\n")             
                if ssn == 'e':
                    return
                #Checks if input is valid
                ssn = int(ssn)
            except:
                print("ssn didn't exist, check if valid format")
                continue
            if self.check_ssn(ssn) == -1:
                print("ssn didn't exist, check if valid format")
                continue
            else:
                while True:
                    try:
                        tpe = input("Choose account type:\n1. debit account 2. savings account 'e' to exit\n")
                        self.ds.get_valid_id("accounts") #Requests valid account id to state
                        acc_id = int(self.__state.readline().strip())+1
                        if tpe == '1' or tpe == '2':
                            if tpe == '1':
                                tpe = "debit account"
                            else:
                                tpe = "savings account" 
                            self.ds.open_account(account(acc_id, tpe, 0), ssn) #Sends request to open account
                            print(f"Account added with account number: {acc_id}")
                            return
                        elif tpe == 'e':
                            return
                        else: 
                            print("Enter valid input")    
                    except:
                        print("Enter valid input")
    #Deposits after inpput of ssn and acc id
    def deposit(self):
        while True:
            ssn = input("Enter ssn to deposit into account. 'e' to exit\n")
            if ssn == 'e':
                return
            if self.check_ssn(ssn) == -1 :
                print("Invalid ssn")
                return
            else:
                self.ds.find_accounts_by_ssn(ssn) #Sends requests for accounts with assigned ssn
                if self.__state.read():
                    self.__state.seek(0)
                    accounts = []
                    for line in self.__state: #Reads through state and adds id's and creates account objects and prints them
                        line = line.strip().split(':')
                        print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
                        accounts.append(account(int(line[0]), line[1], float(line[2])))
                    i = input("Enter id to Deposit to  'e' to exit\n")
                    if i == 'e':
                        return
                    for a in accounts: 
                        if int(i)  == a.id: #Checks if input is valid
                            while True:
                                amount = input("Enter amount to deposit 'e' to exit\n")
                                if amount == 'e':
                                    return    
                                try:
                                    amount = float(amount)
                                    a.change_balance(amount) #Creates a transaction for account with given amount
                                    self.ds.update_account(a) #Sends update request to datasource
                                    transaction(a.id, amount, self.ds)
                                    return
                                except:
                                    print("Enter valid amount please")
                    print("Enter a valid account id please")
                print("No accounts belonging to ssn") 
                return #No accounts belonged to valid ssn so returning to menu
    #Prints accounts of ssn
    def print_accounts(self):
        while True:
            print("Enter ssn. 'e' to exit")
            ssn = input()
            if ssn == 'e':
                return
            if self.check_ssn(ssn) == -1:
                return
            else:
                self.ds.find_accounts_by_ssn(ssn) #Requests accounts to state
                if self.__state.read():
                    self.__state.seek(0)    
                    for line in self.__state:
                        line = line.strip().split(':')
                        print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
                    return
                print("No account belonging to ssn")
                return
    #Withdraw after inpput of ssn and acc id
    def withdraw(self):
        while True:
            print("Enter ssn to withdraw from account. 'e' to exit")
            ssn = input()
            if ssn == 'e':
                return
            if self.check_ssn(ssn) == -1: #Check if input is valid
                print("No customer with that ssn")
                continue
            else:
                self.ds.find_accounts_by_ssn(ssn) #finds accounts with ssn and writes to state
                if self.__state.read(): #Checks whether or not accounts exists with given input
                    self.__state.seek(0)
                    while True:
                        accounts = []
                        for line in self.__state:
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
                                        if a.check_withdraw_eligibility(amount) != -1: #Check whether withdraw amount exceeds balance
                                            a.change_balance(amount) #Changes balance with given amount
                                            self.ds.update_account(a) #Sends update request for account
                                            transaction(a.id, amount, self.ds) #Creates a transaction 
                                            return
                                    except:
                                        print("Enter valid amount please")
                        print("Enter a valid account id please")
                print("No accounts belonging to ssn")
                return  # No accounts belonged to valid ssn so returning to menu
    #Prints customer info by ssn
    def get_customer(self):
        while True:   
            print("Enter ssn to find customer information.   'e' to exit")
            ssn = input()
            if(ssn == 'e'):
                return
            self.ds.find_customer_by_ssn(ssn)
            if self.__state.read(): #Checks if customer exists
                self.__state.seek(0)
                line = self.__state.readline().strip().replace('#', '').split(":")
                print(f"id: {line[0]}  Name: {line[1]}   ssn:{line[2]}")
                return
            else:
                print("No customer with that ssn")                    
    #Closes account for customer after ssn and account id input
    def remove_account(self):
        while True:
            try:
                print("Enter ssn to create account for. 'e' to exit")
                ssn = input()
                if ssn == 'e':
                    return
                #Checks if input is valid
                ssn = int(ssn)
            except:
                print("ssn didn't exist, check if valid format")
                continue
            if self.check_ssn(ssn) == -1:
                print("ssn didn't exist, check if valid format")
                continue
            else:
                while True:
                    self.ds.find_accounts_by_ssn(ssn) #Requests accounts by ssn from datasource
                    if self.__state.read():
                        self.__state.seek(0) 
                        acc_ids = []
                        for line in self.__state: #Reads the requests accounts and prints them
                            line = line.strip().split(':')
                            print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
                            acc_ids.append(line[0])
                        print("Enter id to remove 'e' to exit")
                        i = input()
                        if i == 'e':
                            return
                        if i in acc_ids: 
                            self.ds.remove_account(i) #Removes the account if input is valid
                            return
                        else:
                            print("Enter a valid account id please")
                    print("No accounts belonging to ssn")
                    return
    #Gets all transactions after ssn and account id input
    def get_all_transactions_by_pnr_acc_nr(self):
        while True:
            print("Enter ssn to get all transactions. 'e' to exit")
            ssn = input()
            if ssn == 'e':
                return            
            if self.check_ssn(ssn) == -1:
                print("Invalid input, either ssn doesn't exist or no accounts connected")
                return
            else:
                while True:
                    self.ds.find_accounts_by_ssn(ssn)
                    a = []
                    for line in self.__state:
                        line = line.strip().split(':')
                        print(f"Id:{line[0]} Type:{line[1]} Balance:{line[2]}")
                        a.append(line[0])   
                    print("Enter id to print transactions 'e' to exit")
                    i = input()
                    if i == 'e':
                        return
                    elif i in a:
                        self.ds.find_transactions_by_id(i)
                        print(f"Account: {i}")
                        self.__state.seek(0)
                        for line in self.__state:
                            line = line.strip().split(':')
                            print(f"Date: {line[0]} Amount:{line[1]}")
                        return
                    else:
                        print("Enter a valid account id please")
    #Removes current state and puts file cursor at 0
    def update_state(self):
        self.__state.truncate(0)
        self.__state.seek(0)
    #Checks if ssn is valid
    def check_ssn(self, ssn):
        self.ds.check_valid_ssn(ssn)  # Checks if input is valid
        if open('state.txt', 'r').read(1) == '0':
            print("No customer with entered ssn")
            self.__state.seek(0)
            return -1
        
