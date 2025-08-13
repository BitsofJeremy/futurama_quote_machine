"""Database models for the Futurama Quote Machine.

This module contains all database models and related functionality.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class TimestampMixin:
    """Mixin class that adds timestamp columns to models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="When the record was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="When the record was last updated",
    )


class Quote(db.Model, TimestampMixin):
    """Model representing a Futurama quote.

    Attributes:
        id: Primary key identifier
        quote_text: The actual quote text
        character: Character who said the quote
        created_at: When the quote was created
        updated_at: When the quote was last updated
    """

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True, doc="Primary key")
    quote_text: Mapped[str] = mapped_column(
        Text, nullable=False, doc="The actual quote text"
    )
    character: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True, doc="Character who said the quote"
    )

    def __repr__(self) -> str:
        """String representation of the Quote."""
        return f"<Quote(id={self.id}, character='{self.character}')>"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.quote_text} - {self.character}"

    @property
    def serialize(self) -> Dict[str, Any]:
        """Serialize quote to dictionary for JSON responses.

        Returns:
            Dictionary representation of the quote.
        """
        return {
            "id": self.id,
            "quote_text": self.quote_text,
            "character": self.character,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def get_random_quote(cls) -> Optional["Quote"]:
        """Get a random quote from the database.

        Returns:
            Random Quote instance or None if no quotes exist.
        """
        return cls.query.order_by(db.func.random()).first()

    @classmethod
    def get_by_character(cls, character: str) -> List["Quote"]:
        """Get all quotes by a specific character.

        Args:
            character: Character name to filter by.

        Returns:
            List of Quote instances for the character.
        """
        return cls.query.filter_by(character=character).all()

    @classmethod
    def search_quotes(cls, search_term: str) -> List["Quote"]:
        """Search quotes by text content.

        Args:
            search_term: Term to search for in quote text.

        Returns:
            List of Quote instances containing the search term.
        """
        return cls.query.filter(cls.quote_text.contains(search_term)).all()

    def update(self, **kwargs: Any) -> None:
        """Update quote attributes.

        Args:
            **kwargs: Keyword arguments of attributes to update.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()


# Keep backward compatibility with old naming
Quotes = Quote  # Alias for backward compatibility
