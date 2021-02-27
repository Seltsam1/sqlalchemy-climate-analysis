# Climate app

# Import Flask
from flask import Flask

# Create app
app = Flask(__name__)


# Route for homepage
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to the Climate API!"

if __name__ == "__main__":
    app.run(debug=True)
