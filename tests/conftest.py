"""Pytest configuration and fixtures."""

import pytest
from flask import Flask

from app import create_app
from models import Quote, db


@pytest.fixture
def app() -> Flask:
    """Create application for testing."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_quote(app: Flask) -> Quote:
    """Create a sample quote for testing."""
    with app.app_context():
        quote = Quote(quote_text="Bite my shiny metal ass!", character="Bender")
        db.session.add(quote)
        db.session.commit()
        # Refresh to ensure the instance is bound to the session
        db.session.refresh(quote)
        return quote


@pytest.fixture
def sample_quotes(app: Flask) -> list[Quote]:
    """Create multiple sample quotes for testing."""
    with app.app_context():
        quotes = [
            Quote(quote_text="Good news, everyone!", character="Professor"),
            Quote(quote_text="Bite my shiny metal ass!", character="Bender"),
            Quote(quote_text="I'm gonna build my own theme park!", character="Bender"),
            Quote(quote_text="Sweet zombie Jesus!", character="Professor"),
            Quote(quote_text="Shut up and take my money!", character="Fry"),
        ]

        for quote in quotes:
            db.session.add(quote)

        db.session.commit()

        # Refresh all instances to ensure they're bound to the session
        for quote in quotes:
            db.session.refresh(quote)

        return quotes
