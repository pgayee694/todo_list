from app import db
import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    deadline = db.Column(db.DateTime, index=True)
    priority = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Task {}>'.format(self.name)