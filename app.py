from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# App
app = Flask(__name__)

# Intilize SQLAlchemy and configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    timestamp_creation = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp_updated = db.Column(db.DateTime, default=datetime.utcnow)
    fetched = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f"<Message {self.content} for {self.recipient}>"

@app.route('/')
def home():
    return "Welcome! Service API at your service"

# Run the app
if __name__ == '__main__':
    # Initialize the database and create tables if they don’t exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)