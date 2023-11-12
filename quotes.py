# quotes.py
from flask import Blueprint
from flask_restx import Resource, Api, reqparse

# Local imports
from app import db
from model import Quotes

import logging
logger = logging.getLogger(__name__)

quotes_bp = Blueprint('quotes', __name__, url_prefix="/api")

# For the API docs
quotes = Api(quotes_bp,
          title="FUTURAMA QUOTES",
          description="An API for Futurama quotes.",
          version='0.0.2',
          default="quotes",
          contact="bender@example.com",
          doc='/')


# Helper functions
def get_all_quotes():
    # Get all quotes and order by newest first
    qs = Quotes.query.order_by(Quotes.id.asc()).all()
    return qs


def read_quote(quote_number):
    quote = Quotes.query.filter_by(id=quote_number).first_or_404()
    return quote

# ### Write resources ###

def create_quote(**kwargs):
    # print(kwargs)
    quote = {
        "quote_text": kwargs["quote_text"],
        "character": kwargs["character"],
    }
    q = Quotes(**quote)
    db.session.add(q)
    db.session.commit()
    return q


def update_quote(quote_number, **kwargs):
    quote = Quotes.query.filter_by(id=quote_number).one_or_none()
    quote.update(**kwargs)
    db.session.commit()
    return quote


def delete_quote(quote_number):
    quote = Quotes.query.filter_by(id=quote_number).one_or_none()
    db.session.delete(quote)
    db.session.commit()
    return True


@quotes.route('/quotes')
class AllQuotes(Resource):
    def get(self):
        """ GET a list of all quotes.
        ---
            - This endpoint returns all quotes in the DB
        """
        quotes = get_all_quotes()
        quote_list = []
        for quote in quotes:
            d = {
                "id": quote.id,
                "quote_text": quote.quote_text,
                "character": quote.character
            }
            quote_list.append(d)

        return {"quotes": quote_list}


@quotes.route('/quote')
class OneQuote(Resource):
    """ Provides quotes resource. """

    # This is for getting one quote
    single_quote_parser = reqparse.RequestParser()
    single_quote_parser.add_argument('quote_number',
                                    type=int,
                                    required=True,
                                    help="Enter the quote ID number.")

    # ##### POST PARSER #####
    parser = reqparse.RequestParser()
    # Required
    parser.add_argument('quote_text',
                        type=str,
                        required=True,
                        help="REQUIRED - Enter the Quote")
    parser.add_argument('character',
                        type=str,
                        required=True,
                        help="REQUIRED - Enter the Character Name")

    # ##### PUT PARSER #####
    put_parser = reqparse.RequestParser()
    # Required
    put_parser.add_argument('quote_number',
                            type=int,
                            required=True,
                            help="REQUIRED - Give the quote number you would like to update.")
    put_parser.add_argument('quote_text',
                            type=str,
                            required=True,
                            help="REQUIRED - Enter the Quote")
    put_parser.add_argument('character',
                            type=str,
                            required=True,
                            help="REQUIRED - Enter the Character")

    single_quote = {
        'quote_number': 'Enter a quote number'
    }

    @quotes.expect(single_quote_parser)
    def get(self):
        """
        GET one Quote
        ---
            - Required: a quote number
            - Returns one quote in JSON format
        """
        data = OneQuote.single_quote_parser.parse_args()
        quote_number = data['quote_number']
        quote = read_quote(quote_number=quote_number)
        return quote.serialize

### Write resources ###

    @quotes.expect(parser)
    def post(self):
        """ POST a Quote
        ---
            - Requirements
                - A quote requires at least a description
        """

        # get dictionary from parser
        data = OneQuote.parser.parse_args()
        logger.info(data)

        quote = create_quote(
            quote_text=data['quote_text'],
            character=data['character'],
        )

        logger.info("{0} Added".format(quote))

        return {"created": quote.serialize}, 201

    @quotes.expect(put_parser)
    def put(self):
        """ UPDATE a Quote
        ---
            - Updates a quote
            - Add the data
        """
        # get dictionary from parser
        data = OneQuote.put_parser.parse_args()
        quote_number = data['quote_number']
        quote_text = data['quote_text']
        character = data['character']

        res = update_quote(
            quote_number=quote_number,
            quote_text=quote_text,
            character=character
        )
        return {"updated": res.id}, 201

    @quotes.expect(single_quote_parser)
    def delete(self):
        """ DELETE a Quote
        ---
            - Deletes a quote
            - Required: a quote number
        """
        data = OneQuote.single_quote_parser.parse_args()
        quote_number = data['quote_number']
        res = delete_quote(quote_number=quote_number)

        logger.info("Deleted quote {0}, have a nice day.".format(quote_number))
        return {"deleted": quote_number}, 201
