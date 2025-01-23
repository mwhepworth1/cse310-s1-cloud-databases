# Import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
from api import api_bp

# Create an instance of the Flask class
# The first argument is the name of the application's module or package
app = Flask(__name__)
app.register_blueprint(api_bp)

#######################################
#             FRONT END               #
#######################################

# In-memory storage for to-do items
todo_items = []

# Define a route for the root URL ("/")
@app.route('/')
def home():
    return render_template('index.html', items=todo_items)

# Define a route to add new to-do items
@app.route('/add', methods=['POST'])
def add_item():
    item = request.form.get('item')
    if item:
        todo_items.append(item)
    return redirect(url_for('home'))

# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    app.run(debug=True)