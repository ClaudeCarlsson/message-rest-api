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

@app.route('/fetch_messages', methods=['GET'])
def fetch_messages():
    # Extract start and stop parameters from query string, defaulting to None
    start = request.args.get('start', type=int)
    stop = request.args.get('stop', type=int)
    recipient = request.args.get('recipient')

    # Ensure recipient is provided
    if not recipient:
        return jsonify({"error": "Recipient parameter is required"}), 400

    # Check if recipient exists in the database
    recipient_exists = Message.query.filter_by(recipient=recipient).first()
    if not recipient_exists:
        return jsonify({"error": "Recipient not found in the database"}), 404

    # Query all messages for the recipient, ordered by timestamp
    messages = Message.query.filter_by(recipient=recipient).order_by(Message.timestamp_creation).all()

    # Apply indexing if start and stop are provided
    if start is not None or stop is not None:
        messages = messages[start:stop]
        if messages == []:
            return jsonify({"error": "No message in that range"}), 404 

    # Prepare message data for the response
    message_list = [{ 
        "id": message.id,
        "content": message.content,
        "recipient": message.recipient,
        "timestamp_creation": message.timestamp_creation,
        "timestamp_updated": message.timestamp_updated
    } for message in messages]

    # Return the ordered messages with the specified range
    return jsonify({
        "message": f"Messages for {recipient} retrieved successfully",
        "data": message_list
    }), 200



@app.route('/delete_messages', methods=['DELETE'])
def delete_messages():
    # Parse request data (expecting JSON format)
    data = request.get_json()
    ids = data.get('ids', [])

    # If no IDs are provided, return an error response
    if not ids:
        return jsonify({"error": "IDs list is required"}), 400

    # Track deleted and not found messages
    deleted_ids = []
    not_found_ids = []

    # Loop through provided IDs and attempt to delete each message
    for message_id in ids:
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            deleted_ids.append(message_id)
        else:
            not_found_ids.append(message_id)

    # Commit the changes to the database
    db.session.commit()

    # Return a summary of the deletion process
    return jsonify({
        "message": "Deletion completed",
        "deleted_ids": deleted_ids,
        "not_found_ids": not_found_ids
    }), 200




# Run the app
if __name__ == '__main__':
    # Initialize the database and create tables if they don’t exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)