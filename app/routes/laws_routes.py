from flask import Blueprint, request, jsonify
from app.services.laws_services import search_by_content

laws_routes = Blueprint('laws_routes', __name__)

@laws_routes.route('/laws/search', methods=['GET'])
def route_search_by_content():
    data = search_by_content(request.args)
    return jsonify(data)