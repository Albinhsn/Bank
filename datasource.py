import sqlite3
class datasource:   
    
    def __init__(self): 
        self.db = self.datasource_conn('bank.db')
        self.cur = self.db.cursor()
        self.get_all()
        
    def datasource_conn(self, db_name):
        return sqlite3.connect(db_name)   
    def get_all(self):   
        stmt = "SELECT u.id, u.name, u.scn, a.id, a.type, a.balance FROM user as u , accounts as a WHERE a.holder_id = u.id ORDER BY u.id"
        dct = {}  
        for row in self.cur.execute(stmt):
            if(row[0] not in dct):
                dct[row[0]] = {}
                dct[row[0]]['Name'] = row[1]
                dct[row[0]]['SCN'] = row[2]     
                dct[row[0]]['Account'] = [{'id':row[3],'Type': row[4], 'Balance': row[5]}]
            else:
                dct[row[0]]['Account'].append({'id':row[3],'Type': row[4], 'Balance': row[5]})
        f = open('user_data.txt', 'w')
        for key in dct:
            acc = f"{dct[key]['Account'][0]['id']}:{dct[key]['Account'][0]['Type']}:{dct[key]['Account'][0]['Balance']}"
            lnth = len(dct[key]['Account'])
            if(lnth>1):
                for l in range(lnth-1):
                    l += 1           
                    acc += f"#{dct[key]['Account'][l]['id']}:{dct[key]['Account'][l]['Type']}:{dct[key]['Account'][l]['Balance']}" 
            f.write(f"{key}:{dct[key]['Name']}:{dct[key]['SCN'].replace('-','')}:{acc}\n")
        
        stmt = f"SELECT * FROM user WHERE id NOT IN (SELECT holder_id from accounts)"
        dct = {}
        for row in self.cur.execute(stmt):
                dct[row[0]] = {}
                dct[row[0]]['Name'] = row[1]
                dct[row[0]]['SCN'] = row[2]  
        for key in dct:
            f.write(f"{key}:{dct[key]['Name']}:{dct[key]['SCN'].replace('-','')}\n") 
    def update_by_id(self, dct):
        #{['Type']:"update/insert", ['Table']: '',['id']:id, ['Content']:[(col1,val1),(col2,val2)...]}
        if(dct['Type'] == 'update'):
            cntnt = ''
            for l in len(dct['Content']):
                cntnt += f"{dct['Content'][l][0]} = {dct['Content'][l][1]}"
            stmt = f"""update {dct['Table']} 
                set {cntnt}
                where {dct['id']} = id
            """
            res = []
            for row in self.cur.execute(stmt):
                res.append(row)
            if len(res)>0:
                return res
            else: 
                return -1
        if(dct['Type'] == 'insert'):
            cl = ''
            vl = ''
            for l in len(dct['Content']):
                if(l != len(dct['Content'])-1):
                    vl += f"{(dct['Content'][l][0])},"
                    cl += f"{dct['Content'][l][1]},"
                else:
                    vl += f"{(dct['Content'][l][0])}"
                    cl += f"{dct['Content'][l][1]}"
            stmt = f"""insert into {dct['Table']} ({cl})
                        values ({vl})
            """
            res = [] 
            for row in self.cur.execute(stmt):
                res.append(row)
            if len(res)>0:
                return res
            else: 
                return -1
    def find_by_id(self,id):
        stmt = f'SELECT * FROM USER WHERE id = {id}'
        for row in self.cur.execute(stmt):
            return row  
        return -1
    def remove_by_id(self,id):
        del_stmt = f"DELETE FROM USER WHERE id = {id}"
        get_stmt = f"SELECT * FROM USER WHERE id = {id}"
        res = []
        for row in self.cur.execute(get_stmt):
            res.append(row)
        self.cur.execute(del_stmt)
        try:
            return res[0]
        except:
            return -1