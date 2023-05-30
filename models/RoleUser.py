from sqlalchemy.dialects.mysql import TEXT, INTEGER
from sqlalchemy.sql import func

from flask import request

from config import db
from datetime import datetime


class RoleUser(db.Model):
    __tablename__ = 'role_users'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    role_id = db.Column(INTEGER(unsigned=True),
                        db.ForeignKey('roles.id',
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'),
                        nullable=False,
                        index=True)
    user_id = db.Column(INTEGER(unsigned=True),
                        db.ForeignKey('users.id',
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'),
                        nullable=False,
                        index=True)
    db.UniqueConstraint('role_id', 'user_id')
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, role_id, user_id):
        self.role_id = role_id
        self.user_id = user_id

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'role_id': self.role_id,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }