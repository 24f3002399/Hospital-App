from flask_jwt_extended import JWTManager
from application.models import Users

jwt = JWTManager()

@jwt.user_identity_loader
def load(user):
    return user.email

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header , jwat_data):
    identity = jwat_data["sub"]
    return Users.query.filter_by(email = identity).one_or_none()