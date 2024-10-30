from .submit_route import submit_message
from .fetch_routes import fetch_new_messages, fetch_messages
from .delete_routes import delete_message, delete_messages
from .update_routes import update_message

def init_routes(app):
    app.add_url_rule('/submit_message', view_func=submit_message, methods=['POST'])
    app.add_url_rule('/fetch_new_messages', view_func=fetch_new_messages, methods=['GET'])
    app.add_url_rule('/fetch_messages', view_func=fetch_messages, methods=['GET'])
    app.add_url_rule('/delete_messages', view_func=delete_messages, methods=['DELETE'])
    app.add_url_rule('/delete_message/<int:id>', view_func=delete_message, methods=['DELETE'])
    app.add_url_rule('/update_message', view_func=update_message, methods=['PUT'])
