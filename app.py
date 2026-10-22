from flask import Flask, send_from_directory
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.after_request
def fix_wasm_mime(response):
    if response.headers.get('Content-Type') == 'application/octet-stream':
        response.headers['Content-Type'] = 'application/wasm'
    return response

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

@socketio.on('move')
def on_move(data):
    room = data['room']
    emit('move', data, room=room, include_self=False)

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)