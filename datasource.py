import sqlite3
class datasource:   
    
    def __init__(self): 
        self.__db = self.datasource_conn('bank.db')
    #Queries database for user with ssn and writes 1 if found 0 if not 
    def check_valid_ssn(self, ssn):
        f = open('state.txt', 'w')
        for row in self.__db.execute(f"SELECT * FROM user WHERE ssn = {ssn}"):
            f.write('1')
            f.close()
            return
        f.write('0')
        f.close
    #Inserts a new transaction
    def create_transaction(self, transaction):
        self.__db.execute(f"INSERT INTO transactions VALUES ({transaction.id}, {transaction.account_id}, '{transaction.date}', {transaction.amount})")
        self.__db.commit()    
    #Creates a customer based on customer object c
    def create_customer(self, c):
        self.__db.execute(f"INSERT INTO user VALUES ({c.id}, '{c.name}', {c.ssn})")
        self.__db.commit()
    #Connects to database, database name as parameter db_name
    def datasource_conn(self, db_name):
        return sqlite3.connect(db_name)   
    #Finds a customer and writes it to state
    def find_customer_by_id(self,id):
        l = self.__db.execute(f"SELECT * FROM user WHERE id = {id}").fetchone()
        f = open('state.txt', 'w')
        f.write(f"{l[0]}:{l[1]}:{l[2]}")
        f.close()
    #Finds account(s) by ssn and writes to state
    def find_accounts_by_ssn(self,ssn):
        f = open('state.txt', 'w')
        for row in self.__db.execute(f"SELECT id, type, balance FROM accounts WHERE ssn = {ssn}"):
            line = ""
            for r in row:
                line += str(r) + ":"
            f.write(f"{line[:-1]}\n")
        f.close()
    #Finds customer by ssn and writes to state
    def find_customer_by_ssn(self, ssn):
        try:
            c = self.__db.execute(f"SELECT * FROM user WHERE ssn = {ssn}").fetchone()
            open('state.txt', 'w').write(f"{c[0]}:{c[1]}:{c[2]}")
        except:
            pass
    #Uses a customer object as paramter
    def find_transactions_by_id(self, acc_id):
        f = open('state.txt', 'w')
        for row in self.__db.execute(f"SELECT date, amount FROM transactions WHERE account_id = {acc_id}"):
            s = ""
            for r in row:
                s+= str(r) + ":"
            f.write(f"{s}\n")
        f.close()
    #Queries user table and inits every user as a dict with ssn as key, then queries accounts and adds to account list with corresponding ssn
    def get_all(self):
        dct = {}
        for row in self.__db.execute(f"SELECT * FROM user"):
            dct[row[2]] = {}
            dct[row[2]]['id'] = row[0]
            dct[row[2]]['name'] = row[1]
            dct[row[2]]['account'] = []
        
        for row in self.__db.execute(f"SELECT * FROM accounts"):
            dct[row[1]]['account'].append({'id':row[0], 'tpe':row[2], 'balance':row[3]})
        f = open('state.txt', 'w')
        for key in dct:
            acc = ""
            lnth = len(dct[key]['account'])
            for l in range(lnth):
                acc += f":{dct[key]['account'][l]['id']}:{dct[key]['account'][l]['tpe']}:{dct[key]['account'][l]['balance']}"
            f.write(f"{dct[key]['id']}:{dct[key]['name']}:{key}{acc}\n")
    #Writes the highest valid id to state, table name as paramater
    def get_valid_id(self, table):
        i = self.__db.execute(
            f"SELECT id from {table} order by id desc limit 1").fetchone()[0]
        open('state.txt', 'w').write(str(i))
    #Inserts new account into database, account object and ssn as parameter
    def open_account(self, a, ssn): 
        self.__db.execute(f"INSERT INTO accounts VALUES ({a.id}, {ssn}, '{a.tpe}', {a.balance})")
        self.__db.commit()
    #Removes account and corresponding transaction by id
    def remove_account(self,id):
        b = self.__db.execute(f"SELECT balance from accounts WHERE id = {id}").fetchone()
        print(f"Balance: {b[0]}")        
        self.__db.execute(f"DELETE FROM accounts WHERE id = {id}")
        self.__db.execute(f"DELETE FROM transactions WHERE account_id = {id}")
        self.__db.commit()  
    #Removes customer (and accounts + transactions) by ssn
    def remove_customer_by_ssn(self, ssn):
        acc_ids = []
        for row in self.__db.execute(f"SELECT id FROM accounts WHERE ssn = {ssn}"):
            acc_ids.append(row[0])
        for i in acc_ids:
            self.remove_account(i)         
        self.__db.execute(f"DELETE FROM user WHERE ssn = {ssn}")
        self.__db.commit()
    #Updates a customer object
    def update_customer(self, c):
        self.__db.execute(f"UPDATE user SET name = '{c.name}' WHERE id = {c.id}")
        self.__db.commit()
    #Updates a account object
    def update_account(self, a):
        self.__db.execute(f"UPDATE accounts SET balance = {a.balance} WHERE id = {a.id}")
        self.__db.commit()
