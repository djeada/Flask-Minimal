"""
Modern Flask application entry point using application factory pattern.

This module creates and configures the Flask application using the
application factory pattern for better modularity and testing.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src import create_app

def create_application():
    """Create and configure the Flask application."""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create app using factory pattern
    app = create_app(config_name)
    
    return app


# Create application instance
app = create_application()


if __name__ == "__main__":
    # Development server
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=app.config.get('DEBUG', True)
    )
