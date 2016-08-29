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
twilio_account_sid = "ACacb84763b4ee98385b7e3bebd45422b3" #app.flask_app.config['TWILIO_ACCOUNT_SID']
twilio_auth_token = "36d1a0bc43cf4e1ddfae6d9ddf3add90" #app.flask_app.config['TWILIO_AUTH_TOKEN']
twilio_number = "+12697433810 "#app.flask_app.config['TWILIO_NUMBER']

def draw_something(clientText):
    print(clientText)
    socketio.emit('my response', {'direction': clientText, 'color': 'black'}, namespace='/test')

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
        thread = socketio.start_background_task(target=draw_something("open"))
    global client
    if client is None:
        client = TwilioRestClient(twilio_account_sid,twilio_auth_token)
    #emit('my response', {'data': 'Connected', 'count': 0})

@app.route('/message', methods=['GET', 'POST'])
def stanford_copy():
    clientText = request.args.get('Body').lower()
    draw_something(clientText)
    return ('', 204)

if __name__ == '__main__':
    socketio.run(app, debug=True)
