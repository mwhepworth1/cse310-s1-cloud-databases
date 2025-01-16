from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__) # Acts as a /api prefix for all the below routes.

@api_bp.route('/api', methods=['POST'])
def api():
    data = request.get_json()  # Get the JSON data from the request
    return jsonify({"message": "Data received", "data": data}), 200