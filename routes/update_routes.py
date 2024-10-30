from flask import request, jsonify
from models.message import db, Message
from datetime import datetime

def update_message():
    # Extract parameters from JSON payload
    data = request.get_json()
    message_id = data.get('id')
    content = data.get('content')

    # Ensure id is provided
    if not message_id:
        return jsonify({"error": "Message Id parameter is required"}), 400

    # Check if id exists in the database
    message = Message.query.filter_by(id=message_id).first()
    if not message:
        return jsonify({"error": "Message Id not found in the database"}), 404

    # Update message 
    message.content = content
    message.timestamp_updated = datetime.utcnow()
    db.session.commit()

    # Return success response
    return jsonify({
        "message": f"Message with ID {message_id} updated successfully",
        "data": {
            "id": message.id,
            "content": message.content,
            "recipient": message.recipient,
            "timestamp_creation": message.timestamp_creation,
            "timestamp_updated": message.timestamp_updated
        }
    }), 200