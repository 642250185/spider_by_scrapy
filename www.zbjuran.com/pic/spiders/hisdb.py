import sqlite3

class DemoDB:

    def __del__(self):
        self.conn.close()

    def __init__(self,dbname,flag):
        self.conn = sqlite3.connect(dbname)
        print ("Opened database successfully")
        self.cursor = self.conn.cursor()
        if flag == True:
            self.cursor.execute('''
                create table t_url_list
                (
                    url varchar(1024) primary key ,
                    alt varchar(256),
                    state int ,
                    create_time DATETIME,
                    modify_time DATETIME
                );
                ''')
            print ("Table created successfully")
            self.conn.commit()
            

    def insert(self,url,alt=""):
        try:
            self.cursor.execute("INSERT INTO t_url_list (url,alt,state,create_time,modify_time) \
                VALUES ( \""+url+ "\",\"" +alt+ "\", 0, date('now'),date('now') )")
            self.conn.commit()
            print ("C-CRUD OK:",url)
            return True
        except:
            print ("C-CRUD duplicated:",url)
            return False
    
    def update(self,url):
        try:
            sql = "update t_url_list set state=1 ,modify_time=date('now')\
                where url= \""+url+ "\""
            self.cursor.execute(sql)
            self.conn.commit()
            print ("U-CRUD ok:",url)
            return True
        except:
            print ("U-CRUD error : " ,url)
            return False
    
        
    def query(self,url,state=0):

        sql = "SELECT url,state,create_time,modify_time  from t_url_list where url=\""+url+"\" and state>="+str(state)+";"
        self.cursor.execute(sql)

        res = self.cursor.fetchall()
        #for row in res:
        #    print ("url = ", row[0])
        #    print ("state = ", row[1])
        #    print ("create_time = ", row[2])
        #    print ("modify_time = ", row[3], "\n")

        

        if len(res) > 0:
            #print ("Operation done successfully")
            return True
        else:
            return False

    def query_data(self):

        url =""

        sql = "SELECT url,state,create_time,modify_time  from t_url_list where state = 0 order by create_time limit 1;"
        self.cursor.execute(sql)

        res = self.cursor.fetchall()

        for row in res:
            #print ("url = ", row[0])
            #print ("state = ", row[1])
            #print ("create_time = ", row[2])
            #print ("modify_time = ", row[3], "\n")

            url = row[0]

        

        return url
