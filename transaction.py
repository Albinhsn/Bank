import datetime

class transaction:

    def __init__(self, account_id, amount, ds):
        self.account_id = account_id
        # Creates a date based on current time in format m/d/y
        self.date = datetime.datetime.now().strftime("%m/%d/%y")
        self.amount = amount
        ds.get_valid_id("transactions") #Requests highest used transaction id in state
        self.id = int(open('state.txt', 'r').readline().strip())+1  #reads the requested id and adds 1 to make it valid
        ds.create_transaction(self) #Creates a transaction in database based on object

