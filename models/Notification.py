from sqlalchemy.dialects.mysql import INTEGER, TEXT
from sqlalchemy.sql import func

from config import db


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    client_id = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey('clients.user_id',
                                        ondelete='CASCADE',
                                        onupdate='CASCADE'),
                          nullable=False,
                          index=True,
                          primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    already_seen = db.Column(db.Boolean, nullable=False)

    description = db.Column(TEXT)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, data=None):
        self.already_seen = False
        if data:
            keys = list(data.keys())
            values = list(data.values())
            for i in range(0, len(keys)):
                setattr(self, keys[i], values[i])

    @property
    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
