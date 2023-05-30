from botocore.exceptions import ClientError
from datetime import datetime

from models.Role import Role

class UserHelper:

    def getRoles(user):
        role_ids = [r.role_id for r in user.roles]
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        return [r.serialize['slug'] for r in roles]
