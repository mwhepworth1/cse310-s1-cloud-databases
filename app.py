# pip install flask
# pip install python-dotenv
# pip install mysql.connector
# pip install flask-session

# HOW TO START THE APP:
# python3 app.py
# OR
# python app.py 

# Import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for, session
from api import api_bp
 
# Create an instance of the Flask class
# The first argument is the name of the application's module or package
app = Flask(__name__, static_folder="assets")
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
app.register_blueprint(api_bp)

#######################################
#             FRONT END               #
####################################### 

# In-memory storage for to-do items
todo_items = []

# Define a route for the root URL ("/")
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', items=todo_items, user_id=session.get('user_id'))

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/list/<int:list_id>')
def list(list_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('list.html', list_id=list_id, user_id=session.get('user_id'))

# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    app.run(debug=True)