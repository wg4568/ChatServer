# Start with a basic flask app webpage.
from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request, session, redirect
from random import random
from time import sleep
import json, pickle, os, binascii, pickler

app = Flask(__name__)
app.config['SECRET_KEY'] = binascii.b2a_hex(os.urandom(16))
app.config['DEBUG'] = True
app.config['PICKLE_RESET'] = "KGxwMAou"
app.config['BAD_NAMES'] = ["wg4568"]
app.config['SECRET_PASSWORD'] = "thepassword"

#turn the flask app into a socketio app
socketio = SocketIO(app)

class Reciever():
    def __init__(self):
        self.messages = pickler.load("messages")

    def send(self, user, message):
        if len(message):
            self.messages.insert(0, (user, message))
            pickler.save(self.messages, "messages")
            socketio.emit('newmsg', {'content': message, 'user': user}, namespace='/msg')
            return "Sent from " + user + " that reads, " + message
        else:
            return "Message was blank, not sent"

    def render(self):
#        if not session["VIEW"]:
#            return '<p id="alert"><strong>' + self.messages[0][0] + ': </strong>' + self.messages[0][1] + '</p>'
#        else:
	if 1:
            html = ""
            for msg in self.messages[:session["VIEW"]]:
                if msg[0] == "ALERT":
                    html += '<p id="alert"><strong>' + msg[0] + ': </strong>' + msg[1] + '</p>'
                else:
                    html += '<p><strong>' + msg[0] + ': </strong>' + msg[1] + '</p>'
            return html

rec = Reciever()

@app.before_request
def before_request():
    try: session["VIEW"]
    except KeyError: session["VIEW"] = 0
    try: session["USERNAME"]
    except KeyError: session["USERNAME"] = "AnonUser-" + binascii.b2a_hex(os.urandom(4))
#    if not request.url.split("/")[-1:][0] == "send":
#        rec.send("ALERT", session["USERNAME"] + " has joined the room")

@app.route('/user_newid')
def user_newid():
    session["USERNAME"] = "AnonUser-" + binascii.b2a_hex(os.urandom(4))
    return redirect("/")

@app.route('/user_setid', methods=["POST"])
def user_setname():
    username = request.form["username"]
    canbypass = False
    if username.split("-")[-1:][0] == app.config["SECRET_PASSWORD"]:
        canbypass = True
        username = username.split("-")[0]
    if not username in app.config['BAD_NAMES'] or canbypass:
        session["USERNAME"] = username
    return redirect("/")

@app.route('/send', methods=["POST"])
def send():
    user = request.form["user"]
    content = request.form["content"]
    return rec.send(user, content)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.args.get("viewall"): session["VIEW"] += 10
    else: session["VIEW"] = 0
    print session["VIEW"]
    return render_template('index.html', old=rec.render(), username=session["USERNAME"])

@socketio.on('connect', namespace='/msg')
def test_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/msg')
def test_disconnect():
#    rec.send("ALERT", session["USERNAME"] + " has left the room",)
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
