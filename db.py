import sqlite3



def create_table():
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	elidart.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, email text, name text, user text, password text, code text)")
	elidart.execute("CREATE TABLE IF NOT EXISTS messages(id integer PRIMARY KEY,user text, message text)")
	con.commit()
	con.close()
	return


def save_data(email,name,username,password,code):
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	query = f"SELECT * FROM users WHERE email = '{email}' or user = '{username}'" #si ya hay usuario con esos datos
	if elidart.execute(query).fetchall() == []: #si no hay resultados con esos parametros
		query=  f"INSERT INTO users(email,name,user,password,code) values('{email}','{name}','{username}','{password}', '{code}')"
		elidart.execute(query)
		con.commit()
		con.close()
		return
	else: #si ya existe un usuario registrado 
		return False

def check_data(email,password):
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()
	query = f"select * from users where email = '{email}' and password = '{password}'"
	elidart.execute(query)
	result = elidart.fetchone() #muestra resultados como lista
	con.commit()
	con.close()
	if result == []: #si no hay querys con esos parametros
		return False
	else:
		return result[5] #returns state of 2factor auth


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

def get_nick(email):
	con = sqlite3.connect('users.db', check_same_thread=False)
	elidart = con.cursor()	
	query = elidart.execute(f"SELECT user FROM users where email = '{email}'").fetchone() #obtiene todos los registros
	return query[0]


def check_old_pass(old_pass,email):
	con = sqlite3.connect('users.db', check_same_thread = False)
	elidart = con.cursor()
	query = f"select password from users where email = '{email}' and password = '{old_pass}'"
	result = elidart.execute(query).fetchall()
	con.commit()
	con.close()
	if result == []:
		return False
	else: 
		return True

def save_new_pass(new,email):
	con = sqlite3.connect('users.db', check_same_thread = False)
	elidart = con.cursor()
	query = f"update users set password = '{new}' where email = '{email}'"
	elidart.execute(query)
	con.commit()
	con.close()
	return 
