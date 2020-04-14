
import os
from flask import Flask, current_app, request, jsonify
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from models import RoleUserAssociationModel, UserModel, RoleModel, db
from utils import find_user_and_role, grant_role, withdraw_role
from errors import NoUserFound, NoRoleFound


class DevelopmentConfig:
    DEBUG = True

    # SECRET_KEY = '123456789'
    SQLALCHEMY_DATABASE_URI = 'postgresql://' \
        'postgres:@postgres_db:5432/permissions_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(DevelopmentConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'POSTGRES_SQLALCHEMY_DATABASE_URI')


config = {
    'dev': DevelopmentConfig,
    'prod': ProdConfig}

app = Flask(__name__)
mode = os.getenv('PERMISSION_SERVER_MODE', 'dev')
app.config.from_object(config[mode])

# db = SQLAlchemy(
#     app=app,
#     session_options=dict(
#         expire_on_commit=False))


db.init_app(app)
app.db = db


@app.errorhandler(KeyError)
def handle_keyerror(error):
    return jsonify(
        error=f'Bad request: {str(error)} is not in request'), 400


@app.errorhandler(NoUserFound)
def handle_user_not_found(error):
    return jsonify(
        error=f'Unprocessable entity: user {error.user_name} not found'), 422


@app.errorhandler(NoRoleFound)
def handle_role_not_found(error):
    return jsonify(
        error=f'Unprocessable entity: role {error.role_name} not found'), 422


@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    return jsonify(error='Conflict: Role already has been granted'), 409


@app.route('/permissions', methods=['GET'])
def permissions_get():
    data = request.get_json() or {}
    user_name = data['user_name']
    role_name = data['role_name']

    permissions_query = current_app.db.session.query(
        RoleUserAssociationModel
    ).filter(
        RoleModel.role_name == role_name
    ).filter(
        UserModel.user_name == user_name
    ).filter(and_(
        UserModel.user_id == RoleUserAssociationModel.user_id,
        RoleModel.role_id == RoleUserAssociationModel.role_id))

    result = dict(**data, got_permission=False)
    try:
        permissions_query.one()
    except NoResultFound:
        return jsonify(result), 200
    else:
        result['got_permission'] = True
        return jsonify(result), 200


@app.route('/permissions', methods=['POST'])
def permissions_set():
    data = request.get_json() or {}
    user_name = data['user_name']
    role_name = data['role_name']
    set_role = data.get('set_role', False)

    user, role = find_user_and_role(user_name, role_name)

    if set_role:
        grant_role(user_name, role_name)
        return jsonify(
            message=f'Successfully granted role {role_name} to user '
            f'{user_name}'), 200
    else:
        withdraw_role(user_name, role_name)
        return jsonify(
            message=f'Successfully withdrawn role {role_name} from user '
            f'{user_name}'), 200


@app.route('/roles', methods=['GET'])
def roles_get():
    roles = current_app.db.session.query(RoleModel).all()
    return jsonify(roles=[role.role_name for role in roles]), 200
