import unittest
from app import app, db
from models.message import Message
from datetime import datetime

class MessageApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_submit_message(self):
        response = self.client.post('/submit_message', json={
            'content': 'Hello, World!',
            'recipient': 'john.doe@example.com'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Message submitted successfully')
        self.assertIn('id', data['data'])

    def test_fetch_new_messages(self):
        # Add a message to test fetching
        with app.app_context():
            message = Message(content='New message', recipient='john.doe@example.com')
            db.session.add(message)
            db.session.commit()

        response = self.client.get('/fetch_new_messages?recipient=john.doe@example.com')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'New messages for john.doe@example.com fetched successfully')
        self.assertGreater(len(data['data']), 0)

    def test_fetch_messages_with_range(self):
        response = self.client.get('/fetch_messages?recipient=john.doe@example.com&start=0&stop=2')
        self.assertIn(response.status_code, [200, 404])  # 200 if messages are found, 404 if range is out of bounds
        data = response.get_json()
        if response.status_code == 200:
            self.assertEqual(data['message'], 'Messages for john.doe@example.com retrieved successfully')

    def test_update_message(self):
        # First, add a message to update
        with app.app_context():
            message = Message(content='Old content', recipient='jane.doe@example.com')
            db.session.add(message)
            db.session.commit()
            message_id = message.id

        # Update the message
        response = self.client.put('/update_message', json={
            'id': message_id,
            'content': 'Updated content'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], f'Message with ID {message_id} updated successfully')
        self.assertEqual(data['data']['content'], 'Updated content')

    def test_delete_message(self):
        # Add a message to delete
        with app.app_context():
            message = Message(content='To be deleted', recipient='delete@example.com')
            db.session.add(message)
            db.session.commit()
            message_id = message.id

        # Delete the message
        response = self.client.delete(f'/delete_message/{message_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], f'Message with ID {message_id} deleted successfully')

    def test_delete_multiple_messages(self):
        # Add multiple messages to delete
        with app.app_context():
            message1 = Message(content='Delete me 1', recipient='multi@example.com')
            message2 = Message(content='Delete me 2', recipient='multi@example.com')
            db.session.add(message1)
            db.session.add(message2)
            db.session.commit()
            ids_to_delete = [message1.id, message2.id]

        # Delete the messages
        response = self.client.delete('/delete_messages', json={'ids': ids_to_delete})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Deletion completed')
        self.assertEqual(set(data['deleted_ids']), set(ids_to_delete))

if __name__ == '__main__':
    unittest.main()
