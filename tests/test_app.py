"""Tests for main application functionality."""

import json

import pytest

from app import create_app
from models import Quote, db


class TestApp:
    """Test cases for main application."""

    def test_app_creation(self):
        """Test application factory."""
        app = create_app("testing")
        assert app is not None
        assert app.config["TESTING"] is True

    def test_index_with_quotes(self, client, sample_quote):
        """Test index page with quotes available."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"QUOTE" in response.data

    def test_index_empty_database(self, client):
        """Test index page with no quotes."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"No quotes available" in response.data

    def test_health_check(self, client, sample_quotes):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert data["quote_count"] == 5
        assert "version" in data

    def test_health_check_empty_db(self, client):
        """Test health check with empty database."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert data["quote_count"] == 0

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "not found" in data["error"].lower()


class TestConfiguration:
    """Test configuration classes."""

    def test_development_config(self):
        """Test development configuration."""
        app = create_app("development")
        assert app.config["DEBUG"] is True
        assert app.config["TESTING"] is False

    def test_testing_config(self):
        """Test testing configuration."""
        app = create_app("testing")
        assert app.config["TESTING"] is True
        assert app.config["DEBUG"] is False
        assert "memory" in app.config["SQLALCHEMY_DATABASE_URI"]

    def test_default_config(self):
        """Test default configuration."""
        app = create_app()
        # Should default to development
        assert app.config["DEBUG"] is True
