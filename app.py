# Import the Flask class from the flask module
from flask import Flask
from api import api_bp

# Create an instance of the Flask class
# The first argument is the name of the application's module or package
app = Flask(__name__)

app.register_blueprint(api_bp)

#######################################
#             FRONT END               #
#######################################

# Define a route for the root URL ("/")
@app.route('/')
def home():
    # This function will be called when the root URL is accessed
    return "Welcome to the basic Flask application!"

# Check if the executed file is the main program and run the app
if __name__ == '__main__':
    # Run the Flask application
    # debug=True enables debug mode, which provides detailed error pages and auto-reloads the server on code changes
    app.run(debug=True)
