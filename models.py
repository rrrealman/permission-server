
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy(
    session_options=dict(
        expire_on_commit=False))


class RoleModel(db.Model):

    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(length=128), unique=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())


class UserModel(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(length=128))


class RoleUserAssociationModel(db.Model):

    __tablename__ = 'role_user_associations'

    user_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    role_id = db.Column(
        db.Integer, db.ForeignKey('roles.role_id'), primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())
