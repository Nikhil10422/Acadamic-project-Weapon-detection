import mysql.connector

db_connection = mysql.connector.connect(

host="localhost",

user="root",

password="",

database="users",
port=3308

)
my_database = db_connection.cursor()

sql_statement =  ("INSERT INTO details (name,email) VALUES (%s,%s)")

values = ("charan","hi")

my_database.execute(sql_statement,values)

db_connection.commit()

