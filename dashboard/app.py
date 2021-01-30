import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('streaming.transactions.legit')
def legit(message):
    emit('legit', message, broadcast=True)

@socketio.on('streaming.transactions.fraud')
def fraud(message):
    emit('fraud', message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=os.environ.get("PORT"))





