from http import client
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

from config import db


class SubscriptionTemplateIcon(db.Model):
    __tablename__ = 'subscription_template_icons'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    subscription_template_id = db.Column(INTEGER(unsigned=True),
                                db.ForeignKey('subscription_templates.id',
                                              ondelete='CASCADE',
                                              onupdate='CASCADE'),
                                nullable=False,
                                index=True)
    url = db.Column(db.String(400), nullable=False)
    key = db.Column(db.String(400), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, subscription_template_id, url, key):
        self.subscription_template_id = subscription_template_id
        self.url = url
        self.key = key

    @property
    def serialize(self):
        return {
            'id': self.id,
            'subscription_template_id': self.subscription_template_id,
            'url': self.url,
            'key': self.key,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
