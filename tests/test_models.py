"""Tests for database models."""

from datetime import datetime

import pytest

from models import Quote, db


class TestQuote:
    """Test cases for Quote model."""

    def test_quote_creation(self, app):
        """Test creating a new quote."""
        with app.app_context():
            quote = Quote(quote_text="Bite my shiny metal ass!", character="Bender")
            db.session.add(quote)
            db.session.commit()

            assert quote.id is not None
            assert quote.quote_text == "Bite my shiny metal ass!"
            assert quote.character == "Bender"
            assert isinstance(quote.created_at, datetime)
            assert isinstance(quote.updated_at, datetime)

    def test_quote_repr(self, sample_quote):
        """Test quote string representation."""
        assert "Bender" in repr(sample_quote)
        assert str(sample_quote.id) in repr(sample_quote)

    def test_quote_str(self, sample_quote):
        """Test quote human-readable string."""
        expected = "Bite my shiny metal ass! - Bender"
        assert str(sample_quote) == expected

    def test_quote_serialize(self, sample_quote):
        """Test quote serialization."""
        serialized = sample_quote.serialize

        assert serialized["id"] == sample_quote.id
        assert serialized["quote_text"] == "Bite my shiny metal ass!"
        assert serialized["character"] == "Bender"
        assert "created_at" in serialized
        assert "updated_at" in serialized

    def test_get_random_quote(self, app, sample_quotes):
        """Test getting a random quote."""
        with app.app_context():
            quote = Quote.get_random_quote()
            assert quote is not None
            quote_ids = [q.id for q in sample_quotes]
            assert quote.id in quote_ids

    def test_get_random_quote_empty_db(self, app):
        """Test getting random quote from empty database."""
        with app.app_context():
            quote = Quote.get_random_quote()
            assert quote is None

    def test_get_by_character(self, app, sample_quotes):
        """Test getting quotes by character."""
        with app.app_context():
            bender_quotes = Quote.get_by_character("Bender")
            assert len(bender_quotes) == 2

            for quote in bender_quotes:
                assert quote.character == "Bender"

    def test_search_quotes(self, app, sample_quotes):
        """Test searching quotes by text."""
        with app.app_context():
            money_quotes = Quote.search_quotes("money")
            assert len(money_quotes) == 1
            assert money_quotes[0].quote_text == "Shut up and take my money!"

    def test_update_quote(self, sample_quote):
        """Test updating a quote."""
        original_updated_at = sample_quote.updated_at

        sample_quote.update(
            quote_text="Updated quote text", character="Updated Character"
        )

        assert sample_quote.quote_text == "Updated quote text"
        assert sample_quote.character == "Updated Character"
        assert sample_quote.updated_at > original_updated_at
