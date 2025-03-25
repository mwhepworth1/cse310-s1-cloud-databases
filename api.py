from flask import Blueprint, request, jsonify, session
from utils.db import Database
from mysql.connector import Error
import bcrypt # Have to run pip install bcrypt in terminal before using

api_bp = Blueprint('api', __name__, url_prefix='/api') # Acts as a /api prefix for all the below routes.

db = Database()

@api_bp.route('/list/create', methods=['POST'])
def create_list():
    """
    METHOD: POST /list/create

    Keys
    - user_id (int): ID of the user creating the list
    - name (str): Name of the list

    Returns
    - JSON response with a success message and the created list data
    Example: {"message": "List successfully created.", "data": {...}}
    """
    if db.connect():
        if request.is_json:
            data = request.get_json()
            required_keys = ["user_id", "name"]
            for key in required_keys:
                if key not in data:
                    # Bad Request
                    return jsonify({"error": f"Missing required key: {key}"}), 400

            try:
                # Insert the new list and get the last inserted ID
                query = "INSERT INTO lists (user_id, list_name) VALUES (%s, %s)"
                values = [data["user_id"], data["name"]]
                result = db.query(query, values)

                if result:
                    # Fetch the inserted row's details using LAST_INSERT_ID()
                    query = "SELECT * FROM lists WHERE lists_id = LAST_INSERT_ID()"
                    response = db.query(query)

                    if response:
                        return jsonify({"message": "List successfully created.", "data": response}), 200 # OK
                    else:
                        return jsonify({"error": "Failed to fetch the created list."}), 500 # Internal Server Error
                else:
                    return jsonify({"error": "Failed to create list."}), 500 # Internal Server Error
            except Error as e: 
                print(f"An unexpected error occurred: '{e}'")
                return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
            finally:
                db.close()
        else:
            return jsonify({"error": "Unsupported Media Type. Content-Type must be application/json."}), 415
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/update', methods=['PUT'])
def update_list():
    """
    METHOD: PUT /list/update

    Keys
    - user_id (int): ID of the user updating the list
    - list_id (int): ID of the list to be updated
    - name (str): New name of the list

    Returns
    - JSON response with a success message and the updated list data
    Example: {"message": "List successfully updated.", "data": {...}}
    """
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
    """
    METHOD: DELETE /list/delete

    Keys
    - user_id (int): ID of the user deleting the list
    - list_id (int): ID of the list to be deleted

    Returns
    - JSON response with a success message and the deleted list data
    Example: {"message": "List successfully deleted.", "data": {...}}
    """
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
    """
    METHOD: GET /list/get

    Request Arguments
    - user_id (int): ID of the user (required)
    - list_id (int): ID of the list to be retrieved

    Returns
    - JSON response with a success message and the retrieved list data
    Example: {"message": "List successfully retrieved.", "data": {...}}
    """
    if db.connect():
        user_id = request.args.get('user_id')
        list_id = request.args.get('list_id')
        if not user_id:
            return jsonify({"error": "Missing required query parameter: user_id"}), 400

        try:
            if list_id:
                query = "SELECT * FROM lists WHERE user_id = %s AND lists_id = %s"
                values = [user_id, list_id]
            else:
                query = "SELECT * FROM lists WHERE user_id = %s"
                values = [user_id]
            
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "List(s) successfully retrieved.", "data": result}), 200
            else:
                return jsonify({"error": "No lists found."}), 404
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/tasks/create', methods=['POST'])
def create_element():
    """
    METHOD: POST /list/tasks/create

    Keys
    - list_id (int): ID of the list to which the task belongs
    - title (str): Title of the task
    - description (str): Description of the task

    Returns
    - JSON response with a success message and the created task data
    Example: {"message": "Element successfully created.", "data": {...}}
    """
    if db.connect():
        data = request.get_json()
        required_keys = ["list_id", "title", "description"]
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
    """
    METHOD: PUT /list/tasks/update

    Keys
    - list_id (int): ID of the list to which the task belongs
    - task_id (int): ID of the task to be updated
    - title (str): New title of the task
    - description (str): New description of the task

    Returns
    - JSON response with a success message and the updated task data
    Example: {"message": "Element successfully updated.", "data": {...}}
    """
    if db.connect():
        data = request.get_json()
        required_keys = ["list_id", "title", "description", "task_id"]
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
    """
    METHOD: DELETE /list/tasks/delete

    Keys
    - task_id (int): ID of the task to be deleted

    Returns
    - JSON response with a success message and the deleted task data
    Example: {"message": "Task successfully deleted.", "data": {...}}
    """
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
    """
    METHOD: GET /list/tasks/get

    Request Arguments
    - user_id (int): ID of the user
    - list_id (int): ID of the list to which the task belongs

    Returns
    - JSON response with a success message and the retrieved task data
    Example: {"message": "Task successfully retrieved.", "data": {...}}
    """
    if db.connect():
        user_id = request.args.get('user_id')
        list_id = request.args.get('list_id')
        if not user_id or not list_id:
            return jsonify({"error": "Missing required query parameter: user_id, list_id, or element_id"}), 400
        print(f"User ID: {user_id}, List ID: {list_id}")
        try:
            query = "SELECT * FROM tasks WHERE list_id = %s"
            values = [f'{list_id}']
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "Task successfully retrieved.", "data": result}), 200
            else:
                return jsonify({"error": "Task did not return data.", "data": 0}), 200
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/list/tasks/toggle', methods=['PUT'])
def toggle_element():
    """
    METHOD: PUT /list/tasks/toggle

    Keys
    - user_id (int): ID of the user
    - list_id (int): ID of the list to which the task belongs
    - task_id (int): ID of the task to be toggled

    Returns
    - JSON response with a success message and the toggled task data
    Example: {"message": "Task successfully toggled.", "data": {...}}
    """
    if db.connect():
        data = request.get_json()
        required_keys = [ "list_id", "task_id"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        try: 
            # SET is_done = NOT is_done is the same as "is_done = not is_done" or "is_done = !is_done".
            query = "UPDATE tasks SET is_done = NOT is_done WHERE list_id = %s AND tasks_id = %s"
            values = [data["list_id"], data["task_id"]]
            result = db.query(query, values)
            result += 2
            db.close()
            print(f"Query result: {result - 2}")
            if result:
                return jsonify({"message": "Task successfully toggled.", "data": result - 2}), 200
            
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/user/create', methods=['POST'])
def create_user():
    """
    METHOD: POST /user/create

    Keys
    - username (str): Name accociated with the user
    - password (str): Password associated with the user

    Returns
    - JSON response with a success message
    Example: {"message": "User successfully created."}
    """
    if db.connect():
        data = request.get_json() 
        required_keys = ["username","password"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        try:
            query = "SELECT * FROM users WHERE username = %s"
            values = [data["username"]]
            result = db.query(query, values)
            if result:
                return jsonify({"error": "Username already in use."}), 500
            query = "INSERT INTO users (username, pswd_hash) VALUES (%s, %s)"
            password_byte = data["password"].encode('utf-8')
            hashed = bcrypt.hashpw(password_byte, bcrypt.gensalt())
            values = [data["username"],hashed]
            result = db.query(query, values)
            db.close()
            if result:
                return jsonify({"message": "User successfully created."}), 200 
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

@api_bp.route('/user/verify', methods=['POST'])
def verify_password(): 
    """
    METHOD: POST /user/verify

    Keys
    - username (str): Name accociated with the user
    - password (str): Password associated with the user

    Returns
    - JSON response with a message verifying if the password matches
    Example: {"message": "Password matches."} OR {"message": "Password does not match."}
    """
    if db.connect():
        data = request.get_json() 
        required_keys = ["username","password"]
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        try:
            query = "SELECT pswd_hash, users_id from users WHERE username = %s"
            values = [data["username"]]
            result = db.query(query, values)
            db.close()
            if result:
                stored_hash = result[0]['pswd_hash'].encode('utf-8')
                input_byte = data["password"].encode('utf-8')
                if bcrypt.checkpw(input_byte, stored_hash):
                    session['user_id'] = result[0]['users_id']
                    return jsonify({"message": "Password matches."}), 200
                else:
                    return jsonify({"message": "Password does not match."}), 401
            else:
                return jsonify({"error": "An unexpected error occurred"}), 500
        except Error as e:
            print(f"An unexpected error occurred: '{e}'")
            return jsonify({"error": f"An unexpected error occurred: '{e}'"}), 500
    else:
        return jsonify({"error": "Could not establish connection to database"}), 500

