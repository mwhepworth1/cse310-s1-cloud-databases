from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__) # Acts as a /api prefix for all the below routes.

@api_bp.route('/list/create', methods=['POST'])
def create_list():
    data = request.get_json()  # Get the JSON data from the request
    required_keys = ["user_id", "list_id", "name", "description", "items"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400 # Bad Request
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200 # OK

@api_bp.route('/list/update', methods=['PUT'])
def update_list():
    data = request.get_json()
    required_keys = ["user_id", "list_id", "name", "description", "items"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200

@api_bp.route('/list/delete', methods=['DELETE'])
def delete_list():
    data = request.get_json()
    required_keys = ["user_id", "list_id"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200

@api_bp.route('/list/get', methods=['GET'])
def get_list():
    user_id = request.args.get('user_id')
    list_id = request.args.get('list_id')
    if not user_id or not list_id:
        return jsonify({"error": "Missing required query parameter: user_id or list_id"}), 400
        
    # Query database here

    return jsonify({"message": "Data received", "user_id": user_id, "list_id": list_id}), 200

@api_bp.route('/list/elements/create', methods=['POST'])
def create_element():
    data = request.get_json()
    required_keys = ["user_id", "list_id", "element_id", "element"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200

@api_bp.route('/list/elements/update', methods=['PUT'])
def update_element():
    data = request.get_json()
    required_keys = ["user_id", "list_id", "element_id", "element"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200

@api_bp.route('/list/elements/delete', methods=['DELETE'])
def delete_element():
    data = request.get_json()
    required_keys = ["user_id", "list_id", "element_id"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200

@api_bp.route('/list/elements/get', methods=['GET'])
def get_element():
    user_id = request.args.get('user_id')
    list_id = request.args.get('list_id')
    element_id = request.args.get('element_id')
    if not user_id or not list_id or not element_id:
        return jsonify({"error": "Missing required query parameter: user_id, list_id, or element_id"}), 400
        
    # Query database here

    return jsonify({"message": "Data received", "user_id": user_id, "list_id": list_id, "element_id": element_id}), 200

@api_bp.route('/list/elements/toggle', methods=['PUT'])
def toggle_element():
    data = request.get_json()
    required_keys = ["user_id", "list_id", "element_id"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    # Modify database here

    return jsonify({"message": "Data received", "data": data}), 200
