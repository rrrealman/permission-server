
import functools
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from app import RoleModel, UserModel, RoleUserAssociationModel
from errors import NoRoleFound, NoUserFound


def app_context(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with current_app.app_context():
            return func(*args, **kwargs)

    return wrapper


@app_context
def find_entry(query, exception):
    try:
        return query.one()
    except NoResultFound:
        raise exception


def find_user_and_role(user_name, role_name):
    session = current_app.db.session
    role_query = session.query(RoleModel).filter(
        RoleModel.role_name == role_name)
    role = find_entry(role_query, NoRoleFound(role_name=role_name))
    user_query = session.query(UserModel).filter(
        UserModel.user_name == user_name)
    user = find_entry(user_query, NoUserFound(user_name=user_name))
    return user, role


def grant_role(user_name, role_name):
    user, role = find_user_and_role(user_name, role_name)
    association = RoleUserAssociationModel(
        user_id=user.user_id, role_id=role.role_id)
    current_app.db.session.add(association)
    current_app.db.session.commit()


def withdraw_role(user_name, role_name):
    user, role = find_user_and_role(user_name, role_name)
    current_app.db.session.query(RoleUserAssociationModel).filter(and_(
        RoleUserAssociationModel.role_id == role.role_id,
        RoleUserAssociationModel.user_id == user.user_id)).delete()
    current_app.db.session.commit()
