from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    timestamp_creation = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp_updated = db.Column(db.DateTime, default=datetime.utcnow)
    fetched = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Message {self.content} for {self.recipient}>"
