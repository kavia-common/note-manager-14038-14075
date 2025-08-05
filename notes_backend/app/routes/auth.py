from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..models import db, User
from ..schemas import UserRegisterSchema, UserLoginSchema
from ..auth_utils import generate_jwt

blp = Blueprint("Auth", "auth", url_prefix="/api/auth", description="User authentication routes")

# PUBLIC_INTERFACE
@blp.route("/register")
class Register(MethodView):
    """Register new users."""

    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        """Register a new user (username must be unique)."""
        if User.query.filter_by(username=user_data["username"]).first():
            abort(409, message="Username already exists")
        user = User(username=user_data["username"])
        user.set_password(user_data["password"])
        db.session.add(user)
        db.session.commit()
        token = generate_jwt(user.id)
        return {"message": "User registered successfully", "token": token, "username": user.username}, 201

# PUBLIC_INTERFACE
@blp.route("/login")
class Login(MethodView):
    """User login."""

    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        """Logs in user and returns JWT if successful."""
        user = User.query.filter_by(username=login_data["username"]).first()
        if not user or not user.check_password(login_data["password"]):
            abort(401, message="Invalid username or password")
        token = generate_jwt(user.id)
        return {"token": token, "username": user.username}
