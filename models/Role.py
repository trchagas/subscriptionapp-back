from sqlalchemy.dialects.mysql import TEXT, INTEGER
from sqlalchemy.sql import func

from config import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(INTEGER(unsigned=True), primary_key=True, nullable=False)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(TEXT)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    def __init__(self, slug, description):
        self.slug = slug
        self.description = description

    @property
    def serialize(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
