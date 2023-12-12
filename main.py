from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_cors import CORS
from app.routes.laws_routes import laws_routes
from app.routes.get_data_routes import get_data_routes
from app.socket.event import handle_events

load_dotenv()

app = Flask(__name__)
app.debug = True
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(laws_routes)
app.register_blueprint(get_data_routes)

socketio = handle_events(app)

if __name__ == '__main__':
    socketio.run(app)



