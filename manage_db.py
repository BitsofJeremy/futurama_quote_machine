"""Database management utilities.

This module provides utilities for database initialization and data loading.
"""

import logging
from pathlib import Path
from typing import List, Tuple

from flask import Flask

from app import create_app
from models import Quote, db


def init_database(app: Flask) -> None:
    """Initialize the database schema.

    Args:
        app: Flask application instance.
    """
    with app.app_context():
        db.create_all()
        logging.info("Database schema created successfully")


def load_quotes_from_file(app: Flask, file_path: str = "futurama_quotes.txt") -> int:
    """Load quotes from a text file into the database.

    Args:
        app: Flask application instance.
        file_path: Path to the quotes file.

    Returns:
        Number of quotes loaded.

    Raises:
        FileNotFoundError: If the quotes file doesn't exist.
        ValueError: If quote format is invalid.
    """
    quotes_file = Path(file_path)

    if not quotes_file.exists():
        raise FileNotFoundError(f"Quotes file not found: {file_path}")

    quotes_loaded = 0

    with app.app_context():
        # Clear existing quotes
        Quote.query.delete()
        db.session.commit()
        logging.info("Cleared existing quotes")

        # Load quotes from file
        with quotes_file.open("r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    character, quote_text = parse_quote_line(line)

                    quote = Quote(
                        quote_text=quote_text.strip(), character=character.strip()
                    )

                    db.session.add(quote)
                    quotes_loaded += 1

                except ValueError as e:
                    logging.warning(f"Skipping invalid line {line_num}: {e}")
                    continue

        db.session.commit()
        logging.info(f"Loaded {quotes_loaded} quotes successfully")

    return quotes_loaded


def parse_quote_line(line: str) -> Tuple[str, str]:
    """Parse a quote line in format 'Character: Quote text'.

    Args:
        line: Line to parse.

    Returns:
        Tuple of (character, quote_text).

    Raises:
        ValueError: If line format is invalid.
    """
    if ":" not in line:
        raise ValueError(f"Invalid format: {line}")

    parts = line.split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid format: {line}")

    character, quote_text = parts

    if not character.strip() or not quote_text.strip():
        raise ValueError(f"Empty character or quote: {line}")

    return character.strip(), quote_text.strip()


def add_sample_quotes(app: Flask) -> int:
    """Add sample quotes for testing and development.

    Args:
        app: Flask application instance.

    Returns:
        Number of quotes added.
    """
    sample_quotes = [
        ("Bender", "Bite my shiny metal ass!"),
        ("Bender", "I'm gonna build my own theme park! With blackjack! And hookers!"),
        ("Professor", "Good news, everyone!"),
        ("Professor", "Sweet zombie Jesus!"),
        ("Fry", "Shut up and take my money!"),
        ("Fry", "I can't swallow that!"),
        ("Leela", "Bender, we're trying to save the environment!"),
        ("Zoidberg", "Why not Zoidberg?"),
        ("Hermes", "Sweet three-toed sloth of ice planet Hoth!"),
        ("Scruffy", "Scruffy believes in this company."),
    ]

    with app.app_context():
        # Clear existing quotes
        Quote.query.delete()
        db.session.commit()

        # Add sample quotes
        for character, quote_text in sample_quotes:
            quote = Quote(quote_text=quote_text, character=character)
            db.session.add(quote)

        db.session.commit()
        logging.info(f"Added {len(sample_quotes)} sample quotes")

    return len(sample_quotes)


def get_database_stats(app: Flask) -> dict:
    """Get database statistics.

    Args:
        app: Flask application instance.

    Returns:
        Dictionary with database statistics.
    """
    with app.app_context():
        total_quotes = Quote.query.count()
        characters = db.session.query(Quote.character).distinct().count()

        # Get top characters by quote count
        top_characters = (
            db.session.query(Quote.character, db.func.count(Quote.id))
            .group_by(Quote.character)
            .order_by(db.func.count(Quote.id).desc())
            .limit(5)
            .all()
        )

        return {
            "total_quotes": total_quotes,
            "unique_characters": characters,
            "top_characters": [
                {"character": char, "quote_count": count}
                for char, count in top_characters
            ],
        }


def main() -> None:
    """Main function for running database management tasks."""
    import sys

    app = create_app()

    if len(sys.argv) < 2:
        print("Usage: python manage_db.py <command>")
        print("Commands:")
        print("  init      - Initialize database schema")
        print("  load      - Load quotes from file")
        print("  sample    - Add sample quotes")
        print("  stats     - Show database statistics")
        return

    command = sys.argv[1]

    logging.basicConfig(level=logging.INFO)

    if command == "init":
        init_database(app)
        print("Database initialized successfully")

    elif command == "load":
        try:
            count = load_quotes_from_file(app)
            print(f"Loaded {count} quotes from file")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "sample":
        count = add_sample_quotes(app)
        print(f"Added {count} sample quotes")

    elif command == "stats":
        stats = get_database_stats(app)
        print(f"Total quotes: {stats['total_quotes']}")
        print(f"Unique characters: {stats['unique_characters']}")
        print("Top characters:")
        for char_data in stats["top_characters"]:
            print(f"  {char_data['character']}: {char_data['quote_count']} quotes")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
