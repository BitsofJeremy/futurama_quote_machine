"""API endpoints for quote management.

This module provides RESTful API endpoints for CRUD operations on quotes.
"""

import logging
from typing import Any, Dict, List, Optional

from flask import Blueprint, current_app, jsonify, request
from flask_restx import Api, Namespace, Resource, fields, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models import Quote, db

# Create blueprint
quotes_bp = Blueprint("quotes", __name__)

# Create API instance
api = Api(
    quotes_bp,
    title="Futurama Quotes API",
    description="A RESTful API for managing Futurama quotes with full CRUD operations, search, and filtering",
    version="2.0.0",
    contact="bender@example.com",
    doc="/",
    validate=True,
)

# Create namespace - using default namespace for root routes
quotes_ns = api.namespace("", description="Quote operations", path="/")

# Define API models for documentation
quote_model = api.model(
    "Quote",
    {
        "id": fields.Integer(readonly=True, description="Quote identifier"),
        "quote_text": fields.String(required=True, description="The quote text"),
        "character": fields.String(
            required=True, description="Character who said the quote"
        ),
        "created_at": fields.DateTime(readonly=True, description="Creation timestamp"),
        "updated_at": fields.DateTime(
            readonly=True, description="Last update timestamp"
        ),
    },
)

quote_input_model = api.model(
    "QuoteInput",
    {
        "quote_text": fields.String(required=True, description="The quote text"),
        "character": fields.String(
            required=True, description="Character who said the quote"
        ),
    },
)

quote_list_model = api.model(
    "QuoteList",
    {
        "quotes": fields.List(fields.Nested(quote_model)),
        "total": fields.Integer(description="Total number of quotes"),
        "page": fields.Integer(description="Current page number"),
        "per_page": fields.Integer(description="Quotes per page"),
    },
)

# Request parsers
list_parser = reqparse.RequestParser()
list_parser.add_argument("page", type=int, default=1, help="Page number for pagination")
list_parser.add_argument(
    "per_page", type=int, default=20, help="Number of quotes per page"
)
list_parser.add_argument("character", type=str, help="Filter by character name")
list_parser.add_argument("search", type=str, help="Search quotes by text content")

single_quote_parser = reqparse.RequestParser()
single_quote_parser.add_argument(
    "quote_id", type=int, required=True, help="Quote identifier"
)

quote_input_parser = reqparse.RequestParser()
quote_input_parser.add_argument(
    "quote_text", type=str, required=True, help="The quote text"
)
quote_input_parser.add_argument(
    "character", type=str, required=True, help="Character who said the quote"
)

update_parser = reqparse.RequestParser()
update_parser.add_argument("quote_id", type=int, required=True, help="Quote identifier")
update_parser.add_argument("quote_text", type=str, required=True, help="The quote text")
update_parser.add_argument(
    "character", type=str, required=True, help="Character who said the quote"
)


class QuoteService:
    """Service class for quote operations."""

    @staticmethod
    def get_all_quotes(
        page: int = 1,
        per_page: int = 20,
        character: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get paginated quotes with optional filtering.

        Args:
            page: Page number for pagination.
            per_page: Number of quotes per page.
            character: Filter by character name.
            search: Search term for quote text.

        Returns:
            Dictionary with quotes and pagination info.
        """
        query = Quote.query

        # Apply filters
        if character:
            query = query.filter(Quote.character.ilike(f"%{character}%"))

        if search:
            query = query.filter(Quote.quote_text.ilike(f"%{search}%"))

        # Apply pagination
        pagination = query.paginate(
            page=page,
            per_page=min(per_page, current_app.config["MAX_QUOTES_PER_PAGE"]),
            error_out=False,
        )

        return {
            "quotes": [quote.serialize for quote in pagination.items],
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
        }

    @staticmethod
    def get_quote_by_id(quote_id: int) -> Optional[Quote]:
        """Get quote by ID.

        Args:
            quote_id: Quote identifier.

        Returns:
            Quote instance or None if not found.
        """
        return db.session.get(Quote, quote_id)

    @staticmethod
    def create_quote(quote_text: str, character: str) -> Quote:
        """Create a new quote.

        Args:
            quote_text: The quote text.
            character: Character who said the quote.

        Returns:
            Created Quote instance.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        quote = Quote(quote_text=quote_text.strip(), character=character.strip())
        db.session.add(quote)
        db.session.commit()
        return quote

    @staticmethod
    def update_quote(quote_id: int, quote_text: str, character: str) -> Optional[Quote]:
        """Update an existing quote.

        Args:
            quote_id: Quote identifier.
            quote_text: New quote text.
            character: New character name.

        Returns:
            Updated Quote instance or None if not found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        quote = db.session.get(Quote, quote_id)
        if quote:
            quote.update(quote_text=quote_text.strip(), character=character.strip())
            db.session.commit()
        return quote

    @staticmethod
    def delete_quote(quote_id: int) -> bool:
        """Delete a quote.

        Args:
            quote_id: Quote identifier.

        Returns:
            True if deleted, False if not found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        quote = db.session.get(Quote, quote_id)
        if quote:
            db.session.delete(quote)
            db.session.commit()
            return True
        return False


@quotes_ns.route("/quotes")
class QuoteList(Resource):
    """Resource for quote list operations."""

    @quotes_ns.expect(list_parser)
    @quotes_ns.marshal_with(quote_list_model)
    @quotes_ns.doc(
        "list_quotes",
        responses={200: "Success", 500: "Internal server error"},
        params={
            "page": "Page number for pagination (default: 1)",
            "per_page": "Number of quotes per page (default: 20, max: 100)",
            "character": "Filter by character name (case-insensitive partial match)",
            "search": "Search in quote text (case-insensitive partial match)",
        },
    )
    def get(self) -> Dict[str, Any]:
        """Get all quotes with optional filtering and pagination.

        Returns a paginated list of quotes with optional filtering by character name
        or searching within quote text. Supports standard pagination parameters.
        """
        try:
            args = list_parser.parse_args()
            result = QuoteService.get_all_quotes(
                page=args["page"],
                per_page=args["per_page"],
                character=args["character"],
                search=args["search"],
            )
            current_app.logger.info(f"Retrieved {len(result['quotes'])} quotes")
            return result

        except Exception as e:
            current_app.logger.error(f"Error retrieving quotes: {e}")
            api.abort(500, "Internal server error")

    @quotes_ns.expect(quote_input_model)
    @quotes_ns.marshal_with(quote_model, code=201)
    @quotes_ns.doc("create_quote")
    def post(self) -> Dict[str, Any]:
        """Create a new quote."""
        try:
            data = request.get_json()

            if not data or not data.get("quote_text") or not data.get("character"):
                api.abort(400, "Missing required fields: quote_text and character")

            quote = QuoteService.create_quote(
                quote_text=data["quote_text"], character=data["character"]
            )

            current_app.logger.info(f"Created quote {quote.id}")
            return quote.serialize, 201

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error creating quote: {e}")
            db.session.rollback()
            api.abort(500, "Database error")
        except Exception as e:
            current_app.logger.error(f"Error creating quote: {e}")
            api.abort(500, "Internal server error")


@quotes_ns.route("/<int:quote_id>")
class QuoteResource(Resource):
    """Resource for individual quote operations."""

    @quotes_ns.marshal_with(quote_model)
    @quotes_ns.doc("get_quote")
    def get(self, quote_id: int) -> Dict[str, Any]:
        """Get a quote by ID."""
        quote = QuoteService.get_quote_by_id(quote_id)
        if not quote:
            api.abort(404, f"Quote {quote_id} not found")

        current_app.logger.debug(f"Retrieved quote {quote_id}")
        return quote.serialize

    @quotes_ns.expect(quote_input_model)
    @quotes_ns.marshal_with(quote_model)
    @quotes_ns.doc("update_quote")
    def put(self, quote_id: int) -> Dict[str, Any]:
        """Update a quote."""
        data = request.get_json()

        if not data or not data.get("quote_text") or not data.get("character"):
            api.abort(400, "Missing required fields: quote_text and character")

        try:
            quote = QuoteService.update_quote(
                quote_id=quote_id,
                quote_text=data["quote_text"],
                character=data["character"],
            )

            if not quote:
                api.abort(404, f"Quote {quote_id} not found")

            current_app.logger.info(f"Updated quote {quote_id}")
            return quote.serialize

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error updating quote {quote_id}: {e}")
            db.session.rollback()
            api.abort(500, "Database error")

    @quotes_ns.doc("delete_quote")
    def delete(self, quote_id: int) -> Dict[str, str]:
        """Delete a quote."""
        try:
            deleted = QuoteService.delete_quote(quote_id)

            if not deleted:
                api.abort(404, f"Quote {quote_id} not found")

            current_app.logger.info(f"Deleted quote {quote_id}")
            return {"message": f"Quote {quote_id} deleted successfully"}

        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error deleting quote {quote_id}: {e}")
            db.session.rollback()
            api.abort(500, "Database error")


@quotes_ns.route("/random")
class RandomQuote(Resource):
    """Resource for getting random quotes."""

    @quotes_ns.marshal_with(quote_model)
    @quotes_ns.doc("get_random_quote")
    def get(self) -> Dict[str, Any]:
        """Get a random quote."""
        quote = Quote.get_random_quote()
        if not quote:
            api.abort(404, "No quotes available")

        current_app.logger.debug(f"Retrieved random quote {quote.id}")
        return quote.serialize


@quotes_ns.route("/characters")
class CharacterList(Resource):
    """Resource for getting available characters."""

    @quotes_ns.doc("list_characters")
    def get(self) -> Dict[str, List[str]]:
        """Get list of all characters with quotes."""
        try:
            characters = db.session.query(Quote.character).distinct().all()
            character_list = [char[0] for char in characters]

            current_app.logger.debug(f"Retrieved {len(character_list)} characters")
            return {"characters": sorted(character_list)}

        except Exception as e:
            current_app.logger.error(f"Error retrieving characters: {e}")
            api.abort(500, "Internal server error")
