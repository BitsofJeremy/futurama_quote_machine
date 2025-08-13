"""Tests for API endpoints."""

import json

import pytest

from models import Quote, db


class TestQuoteAPI:
    """Test cases for Quote API endpoints."""

    def test_get_quotes_empty(self, client):
        """Test getting quotes from empty database."""
        response = client.get("/api/quotes/")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["quotes"] == []
        assert data["total"] == 0

    def test_get_quotes_with_data(self, client, sample_quotes):
        """Test getting quotes with data."""
        response = client.get("/api/quotes/")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["quotes"]) == 5
        assert data["total"] == 5

    def test_get_quotes_pagination(self, client, sample_quotes):
        """Test quote pagination."""
        response = client.get("/api/quotes/?page=1&per_page=2")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["quotes"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["per_page"] == 2

    def test_get_quotes_filter_by_character(self, client, sample_quotes):
        """Test filtering quotes by character."""
        response = client.get("/api/quotes/?character=Bender")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["quotes"]) == 2

        for quote in data["quotes"]:
            assert quote["character"] == "Bender"

    def test_get_quotes_search(self, client, sample_quotes):
        """Test searching quotes."""
        response = client.get("/api/quotes/?search=money")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["quotes"]) == 1
        assert "money" in data["quotes"][0]["quote_text"].lower()

    def test_get_quote_by_id(self, client, sample_quote):
        """Test getting a specific quote."""
        response = client.get(f"/api/quotes/{sample_quote.id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["id"] == sample_quote.id
        assert data["quote_text"] == sample_quote.quote_text
        assert data["character"] == sample_quote.character

    def test_get_quote_not_found(self, client):
        """Test getting non-existent quote."""
        response = client.get("/api/quotes/999")
        assert response.status_code == 404

    def test_create_quote(self, client, app):
        """Test creating a new quote."""
        quote_data = {"quote_text": "New test quote", "character": "Test Character"}

        response = client.post(
            "/api/quotes/", data=json.dumps(quote_data), content_type="application/json"
        )
        assert response.status_code == 201

        data = json.loads(response.data)
        assert data["quote_text"] == "New test quote"
        assert data["character"] == "Test Character"
        assert "id" in data

        # Verify in database
        with app.app_context():
            quote = db.session.get(Quote, data["id"])
            assert quote is not None
            assert quote.quote_text == "New test quote"

    def test_create_quote_missing_fields(self, client):
        """Test creating quote with missing fields."""
        # Missing character
        response = client.post(
            "/api/quotes/",
            data=json.dumps({"quote_text": "Test quote"}),
            content_type="application/json",
        )
        assert response.status_code == 400

        # Missing quote_text
        response = client.post(
            "/api/quotes/",
            data=json.dumps({"character": "Test"}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_update_quote(self, client, sample_quote, app):
        """Test updating a quote."""
        update_data = {
            "quote_text": "Updated quote text",
            "character": "Updated Character",
        }

        response = client.put(
            f"/api/quotes/{sample_quote.id}",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["quote_text"] == "Updated quote text"
        assert data["character"] == "Updated Character"

        # Verify in database
        with app.app_context():
            quote = db.session.get(Quote, sample_quote.id)
            assert quote.quote_text == "Updated quote text"

    def test_update_quote_not_found(self, client):
        """Test updating non-existent quote."""
        update_data = {
            "quote_text": "Updated quote text",
            "character": "Updated Character",
        }

        response = client.put(
            "/api/quotes/999",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        assert response.status_code == 404

    def test_delete_quote(self, client, sample_quote, app):
        """Test deleting a quote."""
        quote_id = sample_quote.id

        response = client.delete(f"/api/quotes/{quote_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "deleted successfully" in data["message"]

        # Verify deletion in database
        with app.app_context():
            quote = db.session.get(Quote, quote_id)
            assert quote is None

    def test_delete_quote_not_found(self, client):
        """Test deleting non-existent quote."""
        response = client.delete("/api/quotes/999")
        assert response.status_code == 404

    def test_get_random_quote(self, client, sample_quotes):
        """Test getting a random quote."""
        response = client.get("/api/quotes/random")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "id" in data
        assert "quote_text" in data
        assert "character" in data

    def test_get_random_quote_empty_db(self, client):
        """Test getting random quote from empty database."""
        response = client.get("/api/quotes/random")
        assert response.status_code == 404

    def test_get_characters(self, client, sample_quotes):
        """Test getting list of characters."""
        response = client.get("/api/quotes/characters")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "characters" in data

        characters = data["characters"]
        assert "Bender" in characters
        assert "Professor" in characters
        assert "Fry" in characters
        assert len(characters) == 3  # Unique characters

    def test_get_characters_empty_db(self, client):
        """Test getting characters from empty database."""
        response = client.get("/api/quotes/characters")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["characters"] == []
