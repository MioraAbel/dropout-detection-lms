import mysql.connector
conn=mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='moodle_data')
cursor=conn.cursor(dictionary=True)

cursor.execute("SELECT COUNT(*) as abandons FROM student WHERE niveau_risque = 'élevé' ")
print("Abandons élevé:", cursor.fetchall())

cursor.execute("SELECT COUNT(*) as total FROM student")
print("Total:", cursor.fetchall())
