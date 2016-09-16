#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from twilio.rest import TwilioRestClient
import twilio.twiml

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
client = None
#twilio_account_sid = app.flask_app.config['TWILIO_ACCOUNT_SID']
#twilio_auth_token = app.flask_app.config['TWILIO_AUTH_TOKEN']
#twilio_number = app.flask_app.config['TWILIO_NUMBER']

def draw_something(direction, color):
    print(direction + " " + color)
    if not color:
        color = 'black'
    socketio.emit('my response', {'direction': direction, 'color': color}, namespace='/test')

# def background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     direction = ['up', 'left','down', 'right']
#     color = ['black', 'green', 'purple', 'red']
#     while count<10:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my response',
#                       {'direction': direction[count%4], 'color': color[count%4]},
#                       namespace='/test')

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=draw_something("open", "black"))
    global client
    if client is None:
        client = TwilioRestClient(twilio_account_sid,twilio_auth_token)
    #emit('my response', {'data': 'Connected', 'count': 0})

@app.route('/message', methods=['GET', 'POST'])
def stanford_copy():
    clientText = request.args.get('Body')
    if validateMessage(clientText):
        direction = getDirection(clientText)
        color = getColor(clientText)
        draw_something(direction, color)
    return ('', 204)

def getDirection(text):
    list = text.split(" ")
    direction = list[0].lower()
    return direction

def getColor(text):
    list = text.split(" ")
    if len(list) == 2:
        return list[1].lower()
    return "black"

def validateMessage(text):
    if text is None: return False
    list = text.split(" ")
    if len(list) > 2: return False
    if len(list) <= 0: return False
    direction = list[0].lower()
    if direction not in ["up", "down", "left", "right"]: return False
    return True 

if __name__ == '__main__':
    socketio.run(app, debug=True)
