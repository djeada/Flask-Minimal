"""
Service layer for user management.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from flask import current_app
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from src.exceptions import ConflictError, NotFoundError, ValidationError
from src.extensions import db
from src.models import User


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    def create_user(data: Dict[str, Any]) -> User:
        """Create a new user."""
        # Validate required fields
        required_fields = ["name", "email", "password"]
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"{field} is required")

        # Validate email format
        if "@" not in data["email"]:
            raise ValidationError("Invalid email format")

        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            raise ConflictError("User with this email already exists")

        try:
            user = User.from_dict(data)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ConflictError("User with this email already exists")

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = UserService.get_user_by_email(email)
        if user and user.check_password(password) and user.is_active:
            return user
        return None

    @staticmethod
    def create_access_token(user: User) -> str:
        """Create JWT access token for user."""
        expires = timedelta(hours=current_app.config["JWT_ACCESS_TOKEN_EXPIRES_HOURS"])
        return create_access_token(
            identity=user.id,
            expires_delta=expires,
            additional_claims={"role": user.role},
        )

    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of all users."""
        pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "users": [user.to_dict() for user in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page,
            "per_page": per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        }

    @staticmethod
    def update_user(user_id: int, data: Dict[str, Any]) -> User:
        """Update user information."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        # Update allowed fields
        allowed_fields = ["name", "email", "role", "is_active"]
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        if "password" in data:
            user.set_password(data["password"])

        try:
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise ConflictError("Email already exists")

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete user (soft delete by setting is_active to False)."""
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = False
        db.session.commit()
        return True
