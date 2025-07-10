"""
Database models for the library application.
"""
from datetime import datetime
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from src.extensions import db


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(db.Model, TimestampMixin):
    """User model for library system."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # user, admin
    
    # Relationships
    borrowed_books = db.relationship('BookLoan', back_populates='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password: str) -> None:
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email: bool = False) -> dict:
        """Convert user to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_email:
            data['email'] = self.email
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        user = cls(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'user'),
            is_active=data.get('is_active', True)
        )
        if 'password' in data:
            user.set_password(data['password'])
        return user


class Book(db.Model, TimestampMixin):
    """Book model for library system."""
    
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    isbn = db.Column(db.String(13), unique=True, index=True)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    
    # Relationships
    loans = db.relationship('BookLoan', back_populates='book', lazy='dynamic')
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    def to_dict(self) -> dict:
        """Convert book to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'description': self.description,
            'is_available': self.is_available,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create book from dictionary."""
        return cls(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            year=data.get('year'),
            description=data.get('description'),
            total_copies=data.get('total_copies', 1),
            available_copies=data.get('available_copies', data.get('total_copies', 1))
        )


class BookLoan(db.Model, TimestampMixin):
    """Book loan tracking model."""
    
    __tablename__ = 'book_loans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='borrowed_books')
    book = db.relationship('Book', back_populates='loans')
    
    def __repr__(self):
        return f'<BookLoan {self.user.name} - {self.book.title}>'
    
    def to_dict(self) -> dict:
        """Convert loan to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'user_name': self.user.name,
            'book_title': self.book.title,
            'borrowed_at': self.borrowed_at.isoformat(),
            'due_date': self.due_date.isoformat(),
            'returned_at': self.returned_at.isoformat() if self.returned_at else None,
            'is_returned': self.is_returned,
            'is_overdue': self.is_overdue(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def is_overdue(self) -> bool:
        """Check if loan is overdue."""
        if self.is_returned:
            return False
        return datetime.utcnow() > self.due_date
