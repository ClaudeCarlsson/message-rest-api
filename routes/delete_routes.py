from flask import jsonify, request
from models.message import Message, db

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
        message = db.session.get(Message, message_id)
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

def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": f"Message with ID {id} deleted successfully"}), 200