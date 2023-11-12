# Insert some data into our DB

from datetime import date
from db_model import Session, engine, Base
# Import DB tables
from db_model import Quotes


def add_quotes():
    session = Session()
    try:
        num_rows_deleted1 = session.query(Quotes).delete()
        session.commit()
    except:
        session.rollback()
    # Open our pre-populated quote file
    quote_file = open('futurama_quotes.txt', 'r+')
    # Read all the lines
    lines = quote_file.readlines()
    # Iterate over the lines
    for data in lines:
        # Split the line on the colon
        character, quote = data.split(': ')
        # Find our character
        try:
            # Add the quote, and assign the character
            q = Quotes(quote_text=quote, character=character)
            session.add(q)
            session.commit()
            print("Added: {}".format(data))
        except:
            # We broke something
            print('Frack!')

    session.close()


if __name__ == '__main__':
    add_quotes()
