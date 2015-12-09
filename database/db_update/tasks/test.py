from database import conn_db

con = conn_db()

cur = con.cursor()

cur.execute('select * from whois_sum')

print cur.fetchall()