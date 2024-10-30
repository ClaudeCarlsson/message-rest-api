from flask import request, jsonify
from models.message import db, Message

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