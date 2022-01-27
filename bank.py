from datasource import datasource
import customer
import account
class bank:  
    def __init__(self):
        print("Welcome to the bank!")
        self._load()
        self.__run_system()
    #Checks if ssn is valid
    def __check_ssn(self, ssn):
        try:
            self.ds.check_valid_ssn(ssn)  # Checks if input is valid
        except:
            return -1
        if open('state.txt', 'r').read(1) == '0':
            print("No customer with entered ssn")
            self.__state.seek(0)
            return -1
    
    #Main loop/Main Menu
    def __run_system(self): 
        while True:
            inp = input("1. Print ALL customers\n2. Add customer\n3. Change customer name\n4. Remove customer\n5. Create account\n6. Remove Account\n7. Print transactions by account\n8. Print accounts\n9.Withdraw\n10. Deposit\n11. Print customer info\n'E'. Exit\n")
            if inp == '1':
                customer.print_customers(self.ds, self.__state)
            elif inp == '2':
                customer.create_customer(self.ds, self.__state)
            elif inp == '3':
                customer.change_customer_name(self.ds, self.__state)
            elif(inp == '4'):
                ssn = input("Enter ssn you'd like to remove. 'e' to exit\n")
                if ssn == 'e':
                    return
                customer.remove_customer(ssn, self.ds)
            elif inp == '5':
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
                    if self.__check_ssn(ssn) == -1:
                        print("ssn didn't exist, check if valid format")
                        continue
                    account.create_account(ssn, self.ds, self.__state)
                    break   
            elif inp == '6':
                while True:
                    try:
                        print("Enter ssn to remove account for. 'e' to exit")
                        ssn = input()
                        if ssn == 'e':
                            return
                        #Checks if input is valid
                        ssn = int(ssn)
                    except:
                        print("ssn didn't exist, check if valid format")
                        continue
                    if self.__check_ssn(ssn) == -1:
                        print("ssn didn't exist, check if valid format")
                        continue
                    account.remove_account(ssn, self.ds, self.__state)
                    break
            elif inp == '7':
                while True:
                    print("Enter ssn to get all transactions. 'e' to exit")
                    ssn = input()
                    if ssn == 'e':
                        return
                    if self.__check_ssn(ssn) == -1:
                        print("Invalid input, either ssn doesn't exist or no accounts connected")
                        return
                    customer.get_all_transactions(ssn, self.ds, self.__state) 
            elif inp == '8':
                while True:
                    print("Enter ssn. 'e' to exit")
                    ssn = input()
                    if ssn == 'e':
                        return
                    if self.__check_ssn(ssn) == -1:
                        return
                    account.print_accounts(ssn, self.ds, self.__state)
                    break
            elif inp == '9': 
                while True:
                    print("Enter ssn to withdraw from account. 'e' to exit")
                    ssn = input()
                    if ssn == 'e':
                        return
                    if self.__check_ssn(ssn) == -1:  # Check if input is valid
                        print("No customer with that ssn")
                        continue
                    break
                customer.withdraw(ssn, self.ds, self.__state)
            elif(inp == '10'):
                while True:
                    ssn = input("Enter ssn to deposit into account. 'e' to exit\n")
                    if ssn == 'e':
                        return
                    if self.__check_ssn(ssn) == -1:
                        print("Invalid ssn")
                        continue
                    break
                customer.deposit(ssn, self.ds, self.__state)
            elif(inp == '11'):
                print("Enter ssn to find customer information.   'e' to exit")
                ssn = input()
                if(ssn == 'e'):
                    continue
                customer.get_customer(ssn, self.ds, self.__state)
            elif(inp == 'E'):
                print("Thanks for using the bank")
                exit()
            else:
                print("Wrong input try again")
            self.__update_state() #Removes state file and puts state cursor at position 0 
    #Loads datasource and opens state file
    def _load(self):
        self.ds = datasource()
        self.__state = open('state.txt', 'r+')
    
    #Removes current state and puts file cursor at 0
    def __update_state(self):
        self.__state.truncate(0)
        self.__state.seek(0)
    

