from flask import Blueprint, request, jsonify
from utils.db import Database
from mysql.connector import Error

api_bp = Blueprint('api', __name__, url_prefix='/api') # Acts as a /api prefix for all the below routes.

db = Database()

@api_bp.route('/list/create', methods=['POST'])
def create_list():

    if db.connect():
        data = request.get_json() 
        required_keys = ["user_id", "name"]
        for key in required_keys:
            if key not in data:
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
    if db.connect():
        data = request.get_json()
        required_keys = ["user_id", "list_id", "name"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try:
            query = "UPDATE lists SET list_name = %s WHERE user_id = %s AND lists_id = %s"
            values = [data["name"], data["user_id"], data["list_id"]]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "List successfully updated.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

    

@api_bp.route('/list/delete', methods=['DELETE'])
def delete_list():
    if db.connect():
        data = request.get_json()
        required_keys = ["user_id", "list_id"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try:
            query = "DELETE FROM lists WHERE user_id = %s AND lists_id = %s"
            values = [data["user_id"], data["list_id"]]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "List successfully deleted.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/get', methods=['GET'])
def get_list():
    if db.connect():
        user_id = request.args.get('user_id')
        list_id = request.args.get('list_id')
        if not user_id or not list_id:
            return jsonify({"error": "Missing required query parameter: user_id or list_id"}), 400
    
        try:
            query = "SELECT * FROM lists WHERE user_id = %s AND lists_id = %s"
            values = [user_id, list_id]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "List successfully retrieved.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500


@api_bp.route('/list/tasks/create', methods=['POST'])
def create_element():
    if db.connect():
        data = request.get_json()
        required_keys = ["list_id", "title", "description", "description"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try:
            query = "INSERT INTO tasks (list_id, title, description, is_done) VALUES (%s, %s, %s, %s)"
            values = [data["list_id"], data["title"], data["description"], False]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "Element successfully created.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500


@api_bp.route('/list/tasks/update', methods=['PUT'])
def update_element():
    if db.connect():
        data = request.get_json()
        required_keys = ["list_id", "title", "description"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try:
            query = "UPDATE tasks SET title = %s, description = %s WHERE list_id = %s AND tasks_id = %s"
            values = [data["title"], data["description"], data["list_id"], data["task_id"]]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "Element successfully updated.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/tasks/delete', methods=['DELETE'])
def delete_element():
    if db.connect():
        data = request.get_json()
        required_keys = ["task_id"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try:
            query = "DELETE FROM tasks WHERE tasks_id = %s"
            values = [data["task_id"]]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "Task successfully deleted.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/tasks/get', methods=['GET'])
def get_element():
    if db.connect():
        user_id = request.args.get('user_id')
        list_id = request.args.get('list_id')
        task_id = request.args.get('task_id')
        if not user_id or not list_id or not task_id:
            return jsonify({"error": "Missing required query parameter: user_id, list_id, or element_id"}), 400
        
        try:
            query = "SELECT * FROM tasks WHERE user_id = %s AND list_id = %s AND tasks_id = %s"
            values = [user_id, list_id, task_id]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "Task successfully retrieved.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/tasks/toggle', methods=['PUT'])
def toggle_element():
    if db.connect():
        data = request.get_json()
        required_keys = ["user_id", "list_id", "element_id"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try: 
            # SET is_done = NOT is_done is the same as "is_done = not is_done" or "is_done = !is_done".
            query = "UPDATE tasks SET is_done = NOT is_done WHERE user_id = %s AND list_id = %s AND tasks_id = %s"
            values = [data["user_id"], data["list_id"], data["element_id"]]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "Task successfully toggled.", "data": result}), 200
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500
