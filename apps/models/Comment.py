from . import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, body):
        self.body = body

    def save(self):
        db.session.add(self)
        db.session.commit()

def get_comments_by_timestamp(timestamp):
    return Comment.query.order_by(timestamp).all()
