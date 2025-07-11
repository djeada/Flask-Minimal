"""
Users API endpoints.
"""

from typing import Tuple

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields

from src.api.decorators import admin_required, owner_or_admin_required, validate_json
from src.exceptions import ValidationError as ServiceValidationError
from src.services.user_service import UserService

users_bp = Blueprint("users", __name__)


class UserUpdateSchema(Schema):
    """Schema for user update validation."""

    name = fields.Str(validate=lambda x: len(x) >= 2)
    email = fields.Email()
    role = fields.Str(validate=lambda x: x in ["user", "admin"])
    is_active = fields.Bool()
    password = fields.Str(validate=lambda x: len(x) >= 6)


@users_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def get_users() -> Tuple[Response, int]:
    """Get paginated list of all users (admin only)."""
    try:
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)

        result = UserService.get_all_users(page=page, per_page=per_page)
        return jsonify(result), 200

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to retrieve users"}), 500


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@owner_or_admin_required
def get_user(user_id: int) -> Tuple[Response, int]:
    """Get user by ID (owner or admin only)."""
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user.to_dict(include_email=True)}), 200

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to retrieve user"}), 500


@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@owner_or_admin_required
@validate_json(UserUpdateSchema)
def update_user(user_id: int) -> Tuple[Response, int]:
    """Update user information (owner or admin only)."""
    try:
        data = request.get_json()
        user = UserService.update_user(user_id, data)

        return (
            jsonify(
                {
                    "message": "User updated successfully",
                    "user": user.to_dict(include_email=True),
                }
            ),
            200,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to update user"}), 500


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id: int) -> Tuple[Response, int]:
    """Delete user (admin only)."""
    try:
        UserService.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to delete user"}), 500


@users_bp.route("/<int:user_id>/loans", methods=["GET"])
@jwt_required()
@owner_or_admin_required
def get_user_loans(user_id: int) -> Tuple[Response, int]:
    """Get user's loan history (owner or admin only)."""
    try:
        from src.services.book_service import BookService

        active_only = request.args.get("active_only", "false").lower() == "true"
        loans = BookService.get_user_loans(user_id, active_only=active_only)

        return (
            jsonify({"loans": [loan.to_dict() for loan in loans], "total": len(loans)}),
            200,
        )

    except ServiceValidationError as err:
        return jsonify({"error": str(err)}), err.status_code
    except Exception:
        return jsonify({"error": "Failed to retrieve user loans"}), 500
