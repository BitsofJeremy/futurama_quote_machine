# ### CREATE A DB ###

from datetime import date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Import the db from Flask App
from app import db


class Base(db.Model):
    __abstract__ = True

    # Basics
    id = db.Column(db.Integer, primary_key=True)



class Quotes(Base):
    """ Individual Quote data """
    __tablename__ = 'quotes'

    """
    {
    "id": "Integer",  # created by DB
    "quote_text": "string",
    "character": "string"  
    }
    """
    
    quote_text = Column(String())
    character = Column(String())

    def __init__(self, quote_text, character):
        self.quote_text = quote_text
        self.character = character

    def __repr__(self):
        return "{0} - {1}".format(self.quote_text, self.character)

    @property
    def serialize(self):
        """ Returns a dictionary of the quote information """
        return {
            "id": self.id,
            "quote_text": self.quote_text,
            "character": self.character
        }

