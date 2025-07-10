"""
Authentication API endpoints.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, ValidationError, fields

from src.api.decorators import validate_json
from src.exceptions import UnauthorizedError
from src.exceptions import ValidationError as ServiceValidationError
from src.services.user_service import UserService

auth_bp = Blueprint("auth", __name__)


class LoginSchema(Schema):
    """Schema for login request validation."""

    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)


class RegisterSchema(Schema):
    """Schema for registration request validation."""

    name = fields.Str(required=True, validate=lambda x: len(x) >= 2)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    role = fields.Str(load_default="user", validate=lambda x: x in ["user", "admin"])


@auth_bp.route("/login", methods=["POST"])
@validate_json(LoginSchema)
def login():
    """User login endpoint."""
    try:
        data = request.get_json()
        user = UserService.authenticate_user(data["email"], data["password"])

        if not user:
            raise UnauthorizedError("Invalid credentials")

        access_token = UserService.create_access_token(user)

        return (
            jsonify(
                {"access_token": access_token, "user": user.to_dict(include_email=True)}
            ),
            200,
        )

    except ServiceValidationError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500


@auth_bp.route("/register", methods=["POST"])
@validate_json(RegisterSchema)
def register():
    """User registration endpoint."""
    try:
        data = request.get_json()
        user = UserService.create_user(data)
        access_token = UserService.create_access_token(user)

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "access_token": access_token,
                    "user": user.to_dict(include_email=True),
                }
            ),
            201,
        )

    except ServiceValidationError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get current user information."""
    try:
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(user_id)

        if not user:
            raise UnauthorizedError("User not found")

        return jsonify({"user": user.to_dict(include_email=True)}), 200

    except ServiceValidationError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": "Failed to get user info"}), 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        user_id = get_jwt_identity()
        user = UserService.get_user_by_id(user_id)

        if not user:
            raise UnauthorizedError("User not found")

        access_token = UserService.create_access_token(user)

        return jsonify({"access_token": access_token}), 200

    except ServiceValidationError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": "Token refresh failed"}), 500
