from flask import Flask, request, jsonify
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


@app.route('/submit_message', methods=['POST'])
def submit_message():
    data = request.get_json()
    content = data.get('content')
    recipient = data.get('recipient')

    if not content or not recipient:
        return jsonify({"error": "Both content and recipient are required."}), 400

    new_message = Message(content = content, recipient = recipient)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "message": "Message submitted successfully",
        "data": {
            "id": new_message.id,
            "content": new_message.content,
            "recipient": new_message.recipient,
            "timestamp_creation": new_message.timestamp_creation,
            "timestamp_updated": new_message.timestamp_updated
        }
    }), 201

@app.route('/fetch_new_messages', methods=['GET'])
def fetch_new_messages():
    recipient = request.args.get('recipient')

    # Check that recipient is provided
    if not recipient:
        return jsonify({"error": "Recipient parameter is required"}), 400

    # Check if the recipient exists in the database
    recipient_exists = Message.query.filter_by(recipient=recipient).first()
    if not recipient_exists:
        return jsonify({"error": "Recipient not found in the database"}), 404

    # Query for unfetched messages for this recipient
    messages = Message.query.filter_by(recipient=recipient, fetched=False).all()
    
    # If no new messages, return an empty list
    if not messages:
        return jsonify({"message": "No new messages found", "data":[]}),200

    message_list = []

    for message in messages:
        message_list.append({
            "id": message.id,
            "content": message.content,
            "recipient": message.recipient,
            "timestamp_creation": message.timestamp_creation,
            "timestamp_updated": message.timestamp_updated
        })

        # Mark message as fetched
        message.fetched = True

    # Commit the update to mark messages as fetched
    db.session.commit()

    # Return the fetched messages
    return jsonify({
        "message": f"New messages for {recipient} fetched successfully",
        "data": message_list
    }), 200

# Run the app
if __name__ == '__main__':
    # Initialize the database and create tables if they don’t exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)