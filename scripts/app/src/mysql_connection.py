import mysql.connector
from decouple import config


mydb = mysql.connector.connect(
  host=config('MYSQL_HOST'),
  user=config('MYSQL_USER'),
  password=config('MYSQL_PASSWORD'),
  port=config('MYSQL_PORT'),
  database=config('MYSQL_DATABASE')
)

if mydb.is_connected():
  #print(f"The DataBase is connected on the PORT: {config('MYSQL_PORT')}")
  pass