from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

from config import db


class Admin(db.Model):
    __tablename__ = 'admins'
    user_id = db.Column(INTEGER(unsigned=True),
                        db.ForeignKey('users.id',
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'),
                        nullable=False,
                        index=True,
                        primary_key=True,
                        unique=True)
    name = db.Column(db.String(150), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    subscription_templates = db.relationship('SubscriptionTemplate',
                                             uselist=False,
                                             lazy='select',
                                             backref=db.backref('admin', lazy='joined'))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
