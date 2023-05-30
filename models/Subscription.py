from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, TEXT
from sqlalchemy.sql import func

from config import db


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(INTEGER(unsigned=True), primary_key=True,
                   nullable=False, autoincrement=True)
    client_id = db.Column(INTEGER(unsigned=True),
                          db.ForeignKey('clients.user_id',
                                        ondelete='CASCADE',
                                        onupdate='CASCADE'),
                          nullable=False,
                          index=True,
                          primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    description = db.Column(TEXT)

    price = db.Column(DECIMAL(10, 2), nullable=False)

    next_bill = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())

    billing_cycle = db.Column(INTEGER(unsigned=True))

    remind = db.Column(db.Boolean)

    is_continuous = db.Column(db.Boolean, nullable=False)

    is_active = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    background = db.Column(db.Enum('#FFF001', '#FEC10E', '#F7921E', '#EF6421', '#EB1C24',
                                   '#932490', '#000000', '#642C91', '#0070BA', '#01ABEF',
                                   '#01A99C', '#01A451', '#8BC53D', '#C4C4C4'))

    category = db.Column(db.Enum('music', 'entertainment', 'utilities', 'food_and_beverages',
                         'health_and_wellbeing', 'productivity', 'banking', 'transport', 'education', 'insurance'), nullable=False)

    def __init__(self, data=None):
        self.is_active = True
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
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'next_bill': self.next_bill,
            'billing_cycle': self.billing_cycle,
            'remind': self.remind,
            'is_continuous': self.is_continuous,
            'is_active': self.is_active,
            'background': self.background,
            'category': self.category,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
