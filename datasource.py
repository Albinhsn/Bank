import sqlite3
class datasource:   
    
    def __init__(self): 
        self.__db = self._datasource_conn('bank.db')
    #Queries database for user with ssn and writes 1 if found 0 if not 
    def _check_valid_ssn(self, ssn):
        f = open('state.txt', 'w')
        for row in self.__db.execute(f"SELECT * FROM user WHERE ssn = {ssn}"):
            f.write('1')
            f.close()
            return
        f.write('0')
        f.close
    #Inserts a new transaction
    def _create_transaction(self, transaction):
        self.__db.execute(f"INSERT INTO transactions VALUES ({transaction.id}, {transaction.account_id}, '{transaction.date}', {transaction.amount})")
        self.__db.commit()    
    #Creates a customer based on customer object c
    def _create_customer(self, c):
        self.__db.execute(f"INSERT INTO user VALUES ('{c.name}', {c.ssn})")
        self.__db.commit()
    #Connects to database, database name as parameter db_name
    def _datasource_conn(self, db_name):
        return sqlite3.connect(db_name)   
    #Finds account(s) by ssn and writes to state
    def _find_accounts_by_ssn(self,ssn):
        f = open('state.txt', 'w')
        for row in self.__db.execute(f"SELECT id, type, balance FROM accounts WHERE ssn = {ssn}"):
            line = ""
            for r in row:
                line += str(r) + ":"
            f.write(f"{line[:-1]}\n")
        f.close()
    #Finds customer by ssn and writes to state
    def _find_customer_by_ssn(self, ssn):
        try:
            c = self.__db.execute(f"SELECT * FROM user WHERE ssn = {ssn}").fetchone()
            open('state.txt', 'w').write(f"{c[0]}:{c[1]}")
        except:
            pass
    #Uses a customer object as paramter
    def _find_transactions_by_id(self, acc_id):
        f = open('state.txt', 'w')
        for row in self.__db.execute(f"SELECT date, amount FROM transactions WHERE account_id = {acc_id}"):
            s = ""
            for r in row:
                s+= str(r) + ":"
            f.write(f"{s}\n")
        f.close()
    #Queries user table and inits every user as a dict with ssn as key, then queries accounts and adds to account list with corresponding ssn
    def _get_all(self):
        dct = {}
        for row in self.__db.execute(f"SELECT * FROM user"):
            print(row)
            dct[row[1]] = {'name': row[0], 'account': []}
        
        for row in self.__db.execute(f"SELECT * FROM accounts"):
            dct[row[1]]['account'].append({'id':row[0], 'tpe':row[2], 'balance':row[3]})
        f = open('state.txt', 'w')
        for key in dct:
            acc = ""
            lnth = len(dct[key]['account'])
            for l in range(lnth):
                acc += f":{dct[key]['account'][l]['id']}:{dct[key]['account'][l]['tpe']}:{dct[key]['account'][l]['balance']}"
            f.write(f"{dct[key]['name']}:{key}{acc}\n")
    #Writes the highest valid id to state, table name as paramater
    def _get_valid_id(self, table):
        i = self.__db.execute(
            f"SELECT id from {table} order by id desc limit 1").fetchone()[0]
        open('state.txt', 'w').write(str(i))
    #Inserts new account into database, account object and ssn as parameter
    def _open_account(self, a, ssn): 
        self.__db.execute(f"INSERT INTO accounts VALUES ({a.id}, {ssn}, '{a.tpe}', {a.balance})")
        self.__db.commit()
    #Removes account and corresponding transaction by id
    def _remove_account(self,id):
        b = self.__db.execute(f"SELECT balance from accounts WHERE id = {id}").fetchone()
        print(f"Balance: {b[0]}")        
        self.__db.execute(f"DELETE FROM accounts WHERE id = {id}")
        self.__db.execute(f"DELETE FROM transactions WHERE account_id = {id}")
        self.__db.commit()  
    #Removes customer (and accounts + transactions) by ssn
    def _remove_customer_by_ssn(self, ssn):
        acc_ids = []
        for row in self.__db.execute(f"SELECT id FROM accounts WHERE ssn = {ssn}"):
            acc_ids.append(row[0])
        for i in acc_ids:
            self.remove_account(i)         
        self.__db.execute(f"DELETE FROM user WHERE ssn = {ssn}")
        self.__db.commit()
    #Updates a customer object
    def _update_customer(self, c):
        self.__db.execute(f"UPDATE user SET name = '{c.name}' WHERE ssn = {c.ssn}")
        self.__db.commit()
    #Updates a account object
    def _update_account(self, a):
        self.__db.execute(f"UPDATE accounts SET balance = {a.balance} WHERE id = {a.id}")
        self.__db.commit()
