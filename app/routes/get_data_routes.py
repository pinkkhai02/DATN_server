from flask import Blueprint, request, jsonify
from app.services.get_data_services import scrape_data_content


get_data_routes = Blueprint('get_data_routes', __name__)

@get_data_routes.route('/getcontent', methods=['GET'])
def route_get_data():
    data = scrape_data_content()
    return jsonify(data)

