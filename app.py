"""Main Flask application factory and configuration.

This module contains the application factory pattern implementation
for the Futurama Quote Machine.
"""

import logging
import os
from typing import Optional

from flask import Flask, jsonify, render_template
from flask_migrate import Migrate

from config import get_config
from models import Quote, db


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: Configuration environment name.
                    If None, uses FLASK_ENV environment variable.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Configure logging
    configure_logging(app)

    # Register blueprints
    from api.quotes import quotes_bp

    app.register_blueprint(quotes_bp, url_prefix="/api")

    # Register error handlers
    register_error_handlers(app)

    # Register main routes
    register_routes(app)

    # Initialize configuration
    config_class.init_app(app)

    app.logger.info(f"Application created with {config_class.__name__}")
    return app


def configure_logging(app: Flask) -> None:
    """Configure application logging.

    Args:
        app: Flask application instance.
    """
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))

    # Create formatter
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # Configure handler based on environment
    if app.config.get("LOG_TO_STDOUT"):
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler("app.log")

    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    # Add handler to app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)

    # Log startup message
    app.logger.info("Logging configured successfully")


def register_error_handlers(app: Flask) -> None:
    """Register error handlers for the application.

    Args:
        app: Flask application instance.
    """

    @app.errorhandler(404)
    def not_found_error(error):  # type: ignore
        """Handle 404 errors."""
        app.logger.warning(f"404 error: {error}")
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):  # type: ignore
        """Handle 500 errors."""
        app.logger.error(f"500 error: {error}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(400)
    def bad_request_error(error):  # type: ignore
        """Handle 400 errors."""
        app.logger.warning(f"400 error: {error}")
        return jsonify({"error": "Bad request"}), 400


def register_routes(app: Flask) -> None:
    """Register main application routes.

    Args:
        app: Flask application instance.
    """

    @app.route("/", methods=["GET"])
    def index():  # type: ignore
        """Display a random Futurama quote with character image.

        Returns:
            Rendered HTML template with quote data.
        """
        try:
            quote = Quote.get_random_quote()

            if not quote:
                app.logger.warning("No quotes found in database")
                quote_data = {
                    "quote": "No quotes available! Please add some quotes.",
                    "character": "default.jpg",
                }
            else:
                app.logger.debug(f"Selected quote: {quote.id}")
                quote_data = {
                    "quote": quote.quote_text,
                    "character": f"{quote.character.lower()}.jpg",
                }

            return render_template("index.html", quote=quote_data)

        except Exception as e:
            app.logger.error(f"Error in index route: {e}")
            error_quote = {
                "quote": "Something went wrong! Please try again.",
                "character": "default.jpg",
            }
            return render_template("index.html", quote=error_quote), 500

    @app.route("/health", methods=["GET"])
    def health_check():  # type: ignore
        """Health check endpoint for monitoring.

        Returns:
            JSON response indicating application health.
        """
        try:
            # Test database connection
            quote_count = Quote.query.count()
            return jsonify(
                {"status": "healthy", "quote_count": quote_count, "version": "2.0.0"}
            )
        except Exception as e:
            app.logger.error(f"Health check failed: {e}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500


# Create application instance for development server
app = create_app()


if __name__ == "__main__":
    """Run the application in development mode."""
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", 5000)),
        debug=app.config.get("DEBUG", False),
    )
