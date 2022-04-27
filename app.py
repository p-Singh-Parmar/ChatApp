from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from db import get_user, save_users
import flask_login
from flask_login import LoginManager, current_user, login_required, logout_user


app=Flask(__name__)
app.secret_key='my secret key'
socketio=SocketIO(app)  # it is also encapsulating flask app;
# so a new server will be running where it will be doing the flask side of work as well as running the web sockets
login_manager=LoginManager()
login_manager.login_view='login'   # @login_required requires a login_view and in our case its 'login'
login_manager.init_app(app)   # here i've connected my login-engine with my flask app object


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message=''
    if request.method == 'POST':
        username=request.form.get('username')
        passowrd_input=request.form.get('password')  # We actually get normal passwrd but we have to compare it to hashed passwprd
        user=get_user(username)
        if user and user.checkPassword(passowrd_input):
            flask_login.login_user(user)       # login_user will pass the user object and tell flask to login this user
            return redirect(url_for('home'))
        else:
            message='Failed to login'

    return render_template('login.html', message=message)


@app.route("/logout")
@login_required   # this makes it compulsary for user to login first
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/signup", methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if get_user(username) is None:
            save_users(username, email, password)
        else:
            message='user already exists'
            return render_template('login.html', message=message)
    return render_template('signup.html')

@app.route('/chat')
@login_required # this makes chat available only for authenticated users
def chat():
    username= request.args.get('username')
    room= request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))


# to handle that join_room event we have to create a flask app view
@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined room {}".format(data['username'], data['room']))  # this prints along with time
    # now socketio must be told which socket id is associated with which room
    join_room(data['room'])   # a function inside socketio: it will mae your socket id at particular client join a room
    socketio.emit('join_room_announcement', data)  # it will announce to all other client that someone has joined the room    


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent a message in room {}:{}".format(data['username'],data['room'],data['message']))
    socketio.emit('receive_message', data, room=data['room'])  #sending room id so message is sent to that particular room


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info('{} has left the room {}'.format(data['username'], data['room']))
    leave_room(data['username'], data['room'])
    socketio.emit('leave_room_announcement', data)

# tell flask if this user is already in our database or not
@login_manager.user_loader
def load_user(username):
    return get_user(username)
    

if __name__=="__main__":
    socketio.run(app, debug=True)