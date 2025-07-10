"""
CLI commands for the application.
"""

from typing import Any

import click
from flask import Flask

from src.extensions import db
from src.services.book_service import BookService
from src.services.user_service import UserService


def register_commands(app: Flask) -> None:
    """Register CLI commands."""

    @app.cli.command()
    @click.option("--drop-first", is_flag=True, help="Drop existing tables first")
    def init_db(drop_first: bool) -> None:
        """Initialize the database."""
        if drop_first:
            click.echo("Dropping existing tables...")
            db.drop_all()

        click.echo("Creating database tables...")
        db.create_all()
        click.echo("Database initialized successfully!")

    @app.cli.command()
    def seed_db() -> None:
        """Seed the database with sample data."""
        click.echo("Seeding database with sample data...")

        # Create admin user
        admin_data = {
            "name": "Admin User",
            "email": "admin@library.com",
            "password": "admin123",
            "role": "admin",
        }

        try:
            admin = UserService.create_user(admin_data)
            click.echo(f"Created admin user: {admin.email}")
        except Exception as e:
            click.echo(f"Admin user may already exist: {e}")

        # Create sample users
        sample_users = [
            {
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "password": "password123",
            },
            {
                "name": "Bob Smith",
                "email": "bob@example.com",
                "password": "password123",
            },
            {
                "name": "Charlie Brown",
                "email": "charlie@example.com",
                "password": "password123",
            },
        ]

        for user_data in sample_users:
            try:
                user = UserService.create_user(user_data)
                click.echo(f"Created user: {user.email}")
            except Exception as e:
                click.echo(f'User {user_data["email"]} may already exist: {e}')

        # Create sample books
        sample_books = [
            {
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "year": 1954,
                "isbn": "9780544003415",
                "total_copies": 3,
                "available_copies": 3,
                "description": "Epic fantasy novel about the quest to destroy the One Ring.",
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "year": 1937,
                "isbn": "9780547928227",
                "total_copies": 2,
                "available_copies": 2,
                "description": "A tale of adventure and courage in Middle-earth.",
            },
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "year": 1997,
                "isbn": "9780747532699",
                "total_copies": 5,
                "available_copies": 5,
                "description": "The first book in the Harry Potter series.",
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "year": 1949,
                "isbn": "9780451524935",
                "total_copies": 2,
                "available_copies": 2,
                "description": "A dystopian social science fiction novel.",
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "year": 1960,
                "isbn": "9780061120084",
                "total_copies": 2,
                "available_copies": 2,
                "description": "A novel about racial injustice and childhood innocence.",
            },
        ]

        for book_data in sample_books:
            try:
                book = BookService.create_book(book_data)
                click.echo(f"Created book: {book.title}")
            except Exception as e:
                click.echo(f'Book {book_data["title"]} may already exist: {e}')

        click.echo("Database seeding completed!")

    @app.cli.command()
    @click.option("--email", prompt=True, help="Admin email")
    @click.option("--password", prompt=True, hide_input=True, help="Admin password")
    @click.option("--name", prompt=True, help="Admin name")
    def create_admin(email: str, password: str, name: str) -> None:
        """Create an admin user."""
        admin_data = {
            "name": name,
            "email": email,
            "password": password,
            "role": "admin",
        }

        try:
            admin = UserService.create_user(admin_data)
            click.echo(f"Admin user created successfully: {admin.email}")
        except Exception as e:
            click.echo(f"Failed to create admin user: {e}")
