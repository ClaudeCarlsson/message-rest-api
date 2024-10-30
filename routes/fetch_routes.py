from flask import request, jsonify
from models.message import Message, db

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

def fetch_new_messages():
    # Extract recipient parameter from query string
    recipient = request.args.get('recipient')
    
    # Check that recipient is provided
    if not recipient:
        return jsonify({"error": "Recipient parameter is required"}), 400

    # Query for messages for this recipient that haven’t been fetched
    messages = Message.query.filter_by(recipient=recipient, fetched=False).all()

    # If no new messages, return an empty list
    if not messages:
        return jsonify({"message": "No new messages found", "data": []}), 200

    # Prepare message data for response
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