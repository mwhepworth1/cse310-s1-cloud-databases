# pip install flask
# pip install python-dotenv
# pip install mysql.connector

# HOW TO START THE APP:
# python3 app.py
# OR
# python app.py 

# Import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
from api import api_bp
 
# Create an instance of the Flask class
# The first argument is the name of the application's module or package
app = Flask(__name__, static_folder="assets")
app.register_blueprint(api_bp)

#######################################
#             FRONT END               #
####################################### 

# In-memory storage for to-do items
todo_items = []

# Define a route for the root URL ("/")
@app.route('/')
def home():
    user_id = 1 
    return render_template('index.html', items=todo_items, user_id=user_id)

@app.route('/list/<int:list_id>')
def list(list_id):
    return render_template('list.html', list_id=list_id)

# Define a route to add a new task to a list
@app.route('/add_list_task', methods=['POST'])
def add_list_task():
    list_id = request.form.get('list_id')
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')
    if list_id and task_name and task_description:
        # Here you would typically add the task to your database
        # For now, we'll just append it to the in-memory list for demonstration
        todo_items.append({
            'list_id': list_id,
            'task_name': task_name,
            'task_description': task_description
        })
    return redirect(url_for('list', list_id=list_id))

# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    app.run(debug=True)