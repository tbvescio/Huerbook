import sqlite3



def create_table():
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	elidart.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, email text, name text, user text, password text)")
	elidart.execute("CREATE TABLE IF NOT EXISTS messages(id integer PRIMARY KEY,user text, message text)")
	con.commit()
	con.close()
	return

def save_data(email,name,username,password):
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	query = f"SELECT * FROM users WHERE email = '{email}' or user = '{username}'" #si ya hay usuario con esos datos
	if elidart.execute(query).fetchall() == []: #si no hay resultados con esos parametros
		query=  f"INSERT INTO users(email,name,user,password) values('{email}','{name}','{username}','{password}')"
		elidart.execute(query)
		con.commit()
		con.close()
		return
	else: #si ya existe un usuario registrado 
		return False

def get_messages():
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()	
	query = elidart.execute("SELECT * FROM messages").fetchall() #obtiene todos los registros
	
	users = []
	messages = []
	for row in query:
		messages.append(row[1]) #guarda los mensajes en una lista
		users.append(row[2])
	con.commit()
	con.close()
	return users, messages

def save_messages(user, msg): #guarda los mensajes en la tabla
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	query=  f"INSERT INTO messages(user, message) values('{user}','{msg}')"
	elidart.execute(query)
	con.commit()
	con.close()
	return


def check_data(username,password):
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	query = f"select * from users where user = '{username}' and password = '{password}'"
	elidart.execute(query)
	result = elidart.fetchall() #muestra resultados como lista
	con.commit()
	con.close()
	if result == []: #si no hay querys con esos parametros
		return False
	else:
		return True

def check_old_pass(old_pass,username):
	con = sqlite3.connect('users.db', check_same_thread = False)
	elidart = con.cursor()
	query = f"select password from users where user = '{username}' and password = '{old_pass}'"
	result = elidart.execute(query).fetchall()
	con.commit()
	con.close()
	if result == []:
		return False
	else: 
		return True

def save_new_pass(new,username):
	con = sqlite3.connect('users.db', check_same_thread = False)
	elidart = con.cursor()
	query = f"update users set password = '{new}' where user = '{username}'"
	elidart.execute(query)
	con.commit()
	con.close()
	return 
