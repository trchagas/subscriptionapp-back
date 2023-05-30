from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

from config import db


class SubscriptionTemplate(db.Model):
    __tablename__ = 'subscription_templates'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, nullable=False, autoincrement=True)
    admin_id = db.Column(INTEGER(unsigned=True),
                        db.ForeignKey('admins.user_id',
                                      ondelete='CASCADE',
                                      onupdate='CASCADE'),
                        nullable=False,
                        index=True,
                        primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    icon = db.relationship('SubscriptionTemplateIcon',
                           uselist=False,
                           lazy='select',
                           backref=db.backref('subscription_template', lazy='joined'))

    background = db.Column(db.Enum('#FFF001', '#FEC10E', '#F7921E', '#EF6421', '#EB1C24',
                                   '#932490', '#000000', '#642C91', '#0070BA', '#01ABEF',
                                   '#01A99C', '#01A451', '#8BC53D', '#C4C4C4'), nullable=False)

    category = db.Column(db.Enum('music', 'entertainment', 'utilities', 'food_and_beverages',
                         'health_and_wellbeing', 'productivity', 'banking', 'transport', 'education', 'insurance'))

    def __init__(self, data=None):
        if data:
            keys = list(data.keys())
            values = list(data.values())
            for i in range(0, len(keys)):
                setattr(self, keys[i], values[i])

    @property
    def serialize(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'name': self.name,
            'background': self.background,
            'category': self.category,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
