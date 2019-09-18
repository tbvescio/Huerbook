import sqlite3

con = sqlite3.connect('users.db')
elidart = con.cursor()

def create_table():
	elidart = con.cursor()
	elidart.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, email text, name text, user text, password text)")
	con.commit()
	
def save_data(email,name,username,password):
	con = sqlite3.connect('users.db')
	x =  f"INSERT INTO users(email,name,user,password) values('{email}','{name}','{username}','{password}')"
	elidart.execute(x)
	con.commit()
	con.close()
	return True

def check_data(username,password):
	con = sqlite3.connect('users.db')
	x = f"select * from users where user = '{username}' and password = '{password}'"
	elidart.execute(x)
	result = elidart.fetchall()
	con.commit()
	con.close()
	if result == []:
		return False
	else:
		return True
