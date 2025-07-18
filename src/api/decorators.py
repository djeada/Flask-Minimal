"""
API decorators for validation and authentication.
"""

from functools import wraps
from typing import Any, Callable, Type

from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity
from marshmallow import ValidationError

from src.exceptions import ForbiddenError


def validate_json(schema_class: Type) -> Callable:
    """Decorator to validate JSON request data against a Marshmallow schema."""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            try:
                schema = schema_class()
                data = request.get_json()

                if not data:
                    return jsonify({"error": "No JSON data provided"}), 400

                # Validate data
                validated_data = schema.load(data)

                # Replace request data with validated data
                request._cached_json = validated_data

                return f(*args, **kwargs)

            except ValidationError as err:
                return (
                    jsonify({"error": "Validation failed", "messages": err.messages}),
                    400,
                )
            except Exception:
                return jsonify({"error": "Invalid JSON data"}), 400

        return decorated_function

    return decorator


def admin_required(f: Callable) -> Callable:
    """Decorator to require admin role."""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        try:
            claims = get_jwt()
            user_role = claims.get("role", "user")

            if user_role != "admin":
                raise ForbiddenError("Admin access required")

            return f(*args, **kwargs)

        except ForbiddenError as err:
            return jsonify({"error": str(err)}), err.status_code
        except Exception:
            return jsonify({"error": "Access denied"}), 403

    return decorated_function


def owner_or_admin_required(f: Callable) -> Callable:
    """Decorator to require owner or admin access."""

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        try:
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get("role", "user")
            # Get user_id from URL parameters
            requested_user_id = kwargs.get("user_id")
            # Allow access if admin or owner
            if user_role == "admin" or current_user_id == requested_user_id:
                return f(*args, **kwargs)
            raise ForbiddenError("Access denied: insufficient permissions")
        except ForbiddenError as err:
            return jsonify({"error": str(err)}), err.status_code
        except Exception:
            return jsonify({"error": "Access denied"}), 403

    return decorated_function
