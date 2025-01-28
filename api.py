from flask import Blueprint, request, jsonify
from utils.db import Database
from mysql.connector import Error

api_bp = Blueprint('api', __name__, url_prefix='/api') # Acts as a /api prefix for all the below routes.

db = Database()

@api_bp.route('/list/create', methods=['POST'])
def create_list():

    if db.connect():
        data = request.get_json()  # Get the JSON data from the request
        required_keys = ["user_id", "name"]
        for key in required_keys:
            if key not in data:
                # Bad Request
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try:
            query = "INSERT INTO lists (user_id, list_name) VALUES (%s, %s)"
            values = [data["user_id"], data["name"]]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "List successfully created.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/update', methods=['PUT'])
def update_list():
    data = request.get_json()
    required_keys = ["user_id", "list_id", "name"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400
        
    if db_connection:
        cursor = db_connection.cursor()
        try:
            query = "UPDATE lists SET list_name = %s WHERE user_id = %s AND lists_id = %s"
            values = [data["name"], data["user_id"], data["list_id"]]
            cursor.execute(query, values)
            db_connection.commit()

            return jsonify({"message": "List successfully updated.", "data": data}), 200
        except Error as e:
            print(f"An unexpected error ocurred: '{e}'")
            return jsonify({"error": f"An unexpected error ocurred: '{e}'"}), 500
        finally:
            cursor.close()
            db_connection.close()
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

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
