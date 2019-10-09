from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from db import *
import smtplib, re, hashlib, random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UBH6sOYUiF'
socketio = SocketIO(app) #capsule flask app in socket


@app.route('/' ,methods=['GET','POST'])
def home():
    if 'username' in session: #if there is an user logged in 
        
        #when the cliente requests the page get the messages
        users, messages = get_messages()
       
        return render_template('index.html', username=session['username'], messages=messages, users=users, logueados=logueados)
    else: #if not makes them logged in 
        return redirect('/login')

def recived_message(methods=['GET','POST']):
    print("Message recived!")



@socketio.on('event_message') #happend when recives the event
def handle_event(json, methods=['GET','POST']):
    print("event: " + str(json))

    #when receives the messages stores it in the db
    save_messages(json['user_name'] , json['message'])

    socketio.emit('response', json, callback=recived_message) #callback is debug method




@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET': 
        return render_template('login.html')
    else:
        #extract data from the form
        mail = request.form['mail'] 

        password = request.form['password']
        password = to_hash(password) #makes hash of password

        if user in logueados: #if user is already logged
            print("user loggeed")
            return redirect('/')


        code = check_data(user, password)
        if not x == False: #if data is correct

            code = random.randint(11111,99999)
            send_mail(mail,code=code)
            session['code'] = code

            return render_template('login.html', code=code)

            session['username'] = user
            logueados.append(user)
            print("Los usuarios son:",logueados)


            socketio.emit('users', logueados) #sends users connected to client

            return redirect('/') 
        else:
            return render_template('login.html', error='Datos incorrectos!')        


@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        name = request.form['name']
        user = request.form['user'] 
        password = request.form['password']
        
        try:
            code = request.form['code']
        except:
            code = "off"
        

        if not password == request.form['password2']:
            return render_template('register.html', error='Las contraseñas no son iguales!')

        password = to_hash(password) #makes hash of password

        if email=="" or name=="" or user=="" or password=="": #if there is empty fields
            return render_template('register.html', error='Faltan datos!') 
        elif check_email(email) == False: #if the mail is invalid
            return render_template('register.html', error='Email invalido!') 
        elif save_data(email,name,user,password,code) == False: #if the user is already register
            return render_template('register.html', error='Datos ya registrados!') 
        else: 
            send_mail(email,user)
            return redirect('/login')


@app.route('/logout')
def logout():
    #close session and returns to home page
    logueados.remove(session['username'])
    print("Los usuarios son:" ,logueados)
    session.pop('username', None) #close session    
    socketio.emit('users', logueados) #event where sends connected users
    return redirect('/')



@app.route('/reset', methods = ['POST','GET'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')
    else:
        
        old_pass = to_hash(request.form['old_pass'])
        new_pass = to_hash(request.form['new_pass'])
        email = request.form['email']

        if check_old_pass(old_pass,email) == False: #if there isnt result 
            return render_template('reset_password.html', error = "Contraseña incorrecta")
        else: #if there is an user registered
            save_new_pass(new_pass,email) #saves the new password
            session.pop('username', None)
            return redirect('/login')

    

def to_hash(password):
    password = hashlib.sha224(password.encode()) #make hash with sha224 with data encoded   
    password = password.hexdigest() #convert to hexadecimal

    return password



def send_mail(mail, code=None):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls() #start server
    server.login("WasserSoft@gmail.com","huerbook") #login
    
    if not code:
        msg= """From: WasserSoft
        Subject: Registro Exitoso!
        Gracias por registrarse en nuestra plataforma!
        """
    else:
        msg= """From: WasserSoft
        Subject: Codigo de verificacion!.
        Su codigo de verificacion es {}
        """.format(code)
    server.sendmail("WasserSoft@gmail.com",mail,msg) 


def check_email(mail):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if(re.search(regex,mail)): #if 'mail' contains 'regex' 
        print("Valid Email: ",mail)     
        return True
    else:
        print("Invalid Email: ",mail) 
        return False  

if __name__ == '__main__':
    logueados = []
    create_table()
    socketio.run(app, debug=True)