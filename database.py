from logging import exception
import pymysql
import sys
def database_connect():
    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pymysql.connect(host='localhost',
                        user='caizijian',
                        password='Czj1212112',
                        database = 'Flask')

    except:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        return None

    # return the connection to use
    return connection







def check_login(username, password, email):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #  
        #########


        print(username)
        sql = """
        Select * From UserAccount Where binary username=%s and binary password = %s and binary email = %s
        """
        cur.execute(sql, [username, password, email])
        r = cur.fetchone()

        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None



def check_exist_usr(username, password, repassword,email):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #  
        #########
        # 首先检测是否用户名已被注册
        # 如果已被注册返回“用户已被注册" 如果没有被注册则下一步
        sql1 = """
        Select * From UserAccount Where username=%s;
        """
        cur.execute(sql1, username)
        r = cur.fetchone()
        if r is None:
            # 可以继续
            ps_check = False
            if password == repassword:
                ps_check = True
            if ps_check == True: 
                sql2  = """ INSERT INTO UserAccount VALUES (%s, %s,%s, false); """
                cur.execute(sql2, [username, password,email])
                conn.commit()
                return 1   
            
            return 3
        else:
            return 2
           
         
    except exception as e:
        print(e)
    cur.close()                     # Close the cursor
    conn.close() 
    return None
    

def check_valid_email(username, email):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #  
        #########
        # 首先检测是否用户名已被注册
        # 如果已被注册返回“用户已被注册" 如果没有被注册则下一步

        sql1 = """
        Select email From UserAccount Where binary username=%s;
        """
        cur.execute(sql1, username)
        r = cur.fetchone()

        if r is None:
            # 说明没有账号，账号输入错误
            return 1
        
        if r[0] == email:
            # 说明邮箱是正确邮箱
            return 2
        
        if r[0] != email:
            return 3
            
         
    except exception as e:
        print(e)
    cur.close()                     # Close the cursor
    conn.close() 
    return None
        
        


def set_password(password, username):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #  
        #########
        # 通过用户名来修改密码
        print(password)
        sql1 = """
        UPDATE Flask.UserAccount Set password=%s where binary username =%s;
        """
        cur.execute(sql1, [password,username])
        conn.commit()

    except Exception as e:
        print(e)
        cur.close()                     # Close the cursor
        conn.close() 
        return False
    cur.close()                     # Close the cursor
    conn.close() 
    return True
    