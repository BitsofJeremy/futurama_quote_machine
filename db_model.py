# ### CREATE A DB ###

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///futurama_quote_machine.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


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

    id = Column(Integer, primary_key=True)
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

def main():
  Base.metadata.create_all(engine)
  session = Session()
  session.commit()
  session.close()
  print("Created DB")


if __name__ == '__main__':
    main()
