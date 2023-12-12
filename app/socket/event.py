from flask_socketio import SocketIO
from app.socket.answers import get_answer


def handle_events(app):
    socketio = SocketIO(app, cors_allowed_origins="*")

    @socketio.on('user-send-message')
    def handle_message(data):
        print('received message:', data)
        answer = get_answer(data)
        socketio.emit('bot-answer', answer)

    @socketio.on('connection')
    def handle_connection(data):
        print('--------------connection----------------------')

    @socketio.on('join-chat')
    def join_chat():
        # user_id = generate_random_string(8)
        socketio.emit('res-join-chat', {"user_id": 1})

    return socketio