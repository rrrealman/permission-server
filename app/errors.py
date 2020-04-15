
from sqlalchemy.orm.exc import NoResultFound


class NoRoleFound(NoResultFound):
    def __init__(self, role_name):
        self.role_name = role_name


class NoUserFound(NoResultFound):
    def __init__(self, user_name):
        self.user_name = user_name
