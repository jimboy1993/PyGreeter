# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash

# Define a class to manage user authentication
class UserManager:
    """
    Manages user data and provides methods for authentication.
    """
    def __init__(self):
        """
        Initializes the UserManager with a dictionary of users.
        In a real application, this would connect to a database.
        """
        self.users = {
            "user": "password",  # Example username and password
            "admin": "adminpass",
            "guest": "guestpass"
        }

    def authenticate_user(self, username, password):
        """
        Authenticates a user based on provided username and password.

        Args:
            username (str): The username to check.
            password (str): The password to check.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        if username in self.users and self.users[username] == password:
            return True
        return False

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management and flash messages.
# In a real application, this should be a strong, randomly generated key.
app.secret_key = 'your_secret_key_here' # IMPORTANT: Change this in production!

# Create an instance of the UserManager
user_manager = UserManager()

# Route for the login page (GET request to display the form)
@app.route('/login', methods=['GET'])
def login_form():
    """
    Renders the login form HTML template.
    """
    # Renders 'login.html' which should be in a 'templates' folder.
    return render_template('login.html')

# Route for handling login submission (POST request)
@app.route('/login', methods=['POST'])
def login_submit():
    """
    Handles the login form submission.
    Authenticates the user using the UserManager and redirects to a success page or shows an error.
    """
    username = request.form.get('username') # Get username from the form
    password = request.form.get('password') # Get password from the form

    # Use the UserManager to authenticate the user
    if user_manager.authenticate_user(username, password):
        # If credentials are correct, show a success message
        flash(f'Successfully logged in as {username}!', 'success')
        # In a real app, you would set a session variable here to keep the user logged in.
        return redirect(url_for('dashboard')) # Redirect to a dashboard or home page
    else:
        # If credentials are incorrect, show an error message
        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('login_form')) # Redirect back to the login page

# A simple dashboard page for demonstration after successful login
@app.route('/dashboard')
def dashboard():
    """
    Renders a simple dashboard page.
    This page is shown after a successful login.
    """
    # Retrieve messages flashed from previous requests (e.g., login success/failure)
    messages = request.with_context(lambda: list(app.jinja_env.globals['get_flashed_messages'](with_categories=True)))()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Inter', sans-serif;
                background-color: #f0f4f8;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .card {{
                background-color: #ffffff;
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 90%;
            }}
        </style>
    </head>
    <body>
        <div class="card text-center">
            <h1 class="text-3xl font-bold text-gray-800 mb-6 rounded-md">Welcome to the Dashboard!</h1>
            {"".join([f'<div class="p-3 mb-4 text-sm rounded-md {"bg-green-100 text-green-700" if category == "success" else "bg-red-100 text-red-700"}">{message}</div>' for category, message in messages])}
            <p class="text-gray-600 mb-6">You have successfully logged in.</p>
            <a href="{url_for('login_form')}" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md shadow-md transition duration-300">Logout</a>
        </div>
    </body>
    </html>
    """

# Run the Flask application
if __name__ == '__main__':
    # 'debug=True' allows for automatic reloading on code changes and provides a debugger.
    # Set to False in production for security.
    app.run(debug=True)
