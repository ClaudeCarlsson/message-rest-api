
# Message REST API Service

A simple REST API for sending, retrieving, updating, and deleting messages, built with Flask and SQLAlchemy.

## Features

- **Submit a Message**: Allows users to send a message to a specific recipient.
- **Fetch New Messages**: Retrieves new messages for a recipient, marking them as fetched.
- **Fetch Messages (with Pagination)**: Retrieves all messages for a recipient with optional pagination.
- **Delete Messages**: Deletes single or multiple messages by ID.
- **Update Message**: Updates the content of a specific message.

## Project Structure

```
message-rest-api/
├── app.py                   # Main application entry point
├── config.py                # Configuration file
├── models/
│   └── message.py           # Message model definition
├── routes/
│   ├── __init__.py          # Initializes routes
│   ├── submit_route.py      # Route for submitting messages
│   ├── fetch_routes.py      # Routes for fetching messages
│   ├── delete_routes.py     # Routes for deleting messages
│   └── update_routes.py     # Route for updating messages
├── messages.db              # SQLite database file (auto-generated)
└── test_app.py              # Automated unit tests
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/your-username/message-rest-api.git](https://github.com/ClaudeCarlsson/message-rest-api)
   cd message-rest-api
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   Run the application once to initialize the database:
   ```bash
   python app.py
   ```

## Usage

### Starting the Server

Run the application with:
```bash
python app.py
```

The server will be available at `http://127.0.0.1:5000`.

### API Endpoints

#### 1. Submit a Message
- **Endpoint**: `/submit_message`
- **Method**: `POST`
- **Curl Command**:
  ```bash
  curl -X POST http://127.0.0.1:5000/submit_message -H "Content-Type: application/json" -d '{"content": "Hello, World!", "recipient": "john.doe@example.com"}'
  ```
- **Response**:
  ```json
  {
    "message": "Message submitted successfully",
    "data": {
        "id": 1,
        "content": "Hello, World!",
        "recipient": "john.doe@example.com",
        "timestamp_creation": "2024-10-30T12:00:00",
        "timestamp_updated": "2024-10-30T12:00:00"
    }
  }
  ```

#### 2. Fetch New Messages
- **Endpoint**: `/fetch_new_messages`
- **Method**: `GET`
- **Curl Command**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/fetch_new_messages?recipient=john.doe@example.com"
  ```
- **Response**:
  ```json
  {
    "message": "New messages for john.doe@example.com fetched successfully",
    "data": [
        {
            "id": 1,
            "content": "Hello, World!",
            "recipient": "john.doe@example.com",
            "timestamp_creation": "2024-10-30T12:00:00",
            "timestamp_updated": "2024-10-30T12:00:00"
        }
    ]
  }
  ```

#### 3. Fetch Messages (with Pagination)
- **Endpoint**: `/fetch_messages`
- **Method**: `GET`
- **Curl Command**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/fetch_messages?recipient=john.doe@example.com&start=0&stop=2"
  ```
- **Response**:
  ```json
  {
    "message": "Messages for john.doe@example.com retrieved successfully",
    "data": [
        {
            "id": 1,
            "content": "Hello, World!",
            "recipient": "john.doe@example.com",
            "timestamp_creation": "2024-10-30T12:00:00",
            "timestamp_updated": "2024-10-30T12:00:00"
        }
    ]
  }
  ```

#### 4. Delete a Single Message
- **Endpoint**: `/delete_message/<id>`
- **Method**: `DELETE`
- **Curl Command**:
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/delete_message/1"
  ```
- **Response**:
  ```json
  {
    "message": "Message with ID 1 deleted successfully"
  }
  ```

#### 5. Delete Multiple Messages
- **Endpoint**: `/delete_messages`
- **Method**: `DELETE`
- **Curl Command**:
  ```bash
  curl -X DELETE "http://127.0.0.1:5000/delete_messages" -H "Content-Type: application/json" -d '{"ids": [1, 2, 3]}'
  ```
- **Response**:
  ```json
  {
    "message": "Deletion completed",
    "deleted_ids": [1, 2],
    "not_found_ids": [3]
  }
  ```

#### 6. Update a Message
- **Endpoint**: `/update_message`
- **Method**: `PUT`
- **Curl Command**:
  ```bash
  curl -X PUT "http://127.0.0.1:5000/update_message" -H "Content-Type: application/json" -d '{"id": 1, "content": "Updated Content Here"}'
  ```
- **Response**:
  ```json
  {
    "message": "Message with ID 1 updated successfully",
    "data": {
        "id": 1,
        "content": "Updated Content Here",
        "recipient": "john.doe@example.com",
        "timestamp_creation": "2024-10-30T12:00:00",
        "timestamp_updated": "2024-10-30T12:10:00"
    }
  }
  ```

## Running Tests

To run unit tests, execute:
```bash
python -m unittest test_app.py
```

## License

This project is licensed under the MIT License.
