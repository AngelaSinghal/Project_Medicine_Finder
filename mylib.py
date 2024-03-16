import pymysql

def db_connection():
    con=pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                                         autocommit=True)
    cur = con.cursor()
    return cur
def check_photo(email):
    con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="aarav",
                          autocommit=True)
    cur = con.cursor()
    cur.execute("select * from photodata where email='"+email+"'")
    n=cur.rowcount
    photo="no"
    if (n>0):
        row = cur.fetchone()
        photo = row[1]

    return photo