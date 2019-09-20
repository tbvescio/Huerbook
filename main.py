from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from db import save_data, check_data, create_table, save_messages,get_messages

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UBH6sOYUiF'
socketio = SocketIO(app) #capsule flask app in socket


create_table()

@app.route('/')
def home():
    if 'username' in session: #if there is an user logged in 
        
        #when the cliente requests the page get the messages
        messages = get_messages()
       
        return render_template('index.html', username=session['username'], messages=messages)
    else: #if not makes them logged in 
        return redirect('/login')

def recived_message(methods=['GET','POST']):
    print("Message recived!")



@socketio.on('event_message') #happend when recives the event
def handle_event(json, methods=['GET','POST']):
    print("event: " + str(json))

    #when receives the messages stores it in the db
    save_messages(json['user_name'] + ":" + json['message'])

    socketio.emit('response', json, callback=recived_message) #callback is debug method



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET': 
        return render_template('login.html')
    else:
        #extract data from the form
        user = request.form['user'] 
        password = request.form['password']

        if check_data(user, password) == True: #if data is correct
            session['username'] = user #saves the name of the user in the session
            return redirect('/') #redirect to home page
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

        if email=="" or name=="" or user=="" or password=="": #if there is empty fields
            return render_template('register.html', error='Faltan datos!') 

        if save_data(email,name,user,password) == False:
            return render_template('register.html', error='Datos ya registrados!') 
        else:
            return redirect('/login')


@app.route('/logout')
def logout():
    #close session and returns to home page
    session.pop('username', None)
    return redirect('/') 




if __name__ == '__main__':
    socketio.run(app, debug=True)