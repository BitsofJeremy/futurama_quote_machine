# app.py

# Main App Entry Point
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import random

# Define the user DB
db = SQLAlchemy()

app = Flask(__name__)
# Pull in the config
app.config.from_pyfile('config.py')

# Setup the app db
db.init_app(app)
# Migrate DB to fix any changes
migrate = Migrate(app, db)
from model import Quotes

#  ### Blueprints ###

# Initial frontend views
from quotes import quotes_bp
# Register the Blueprints with the app
app.register_blueprint(quotes_bp)


# ### Set up logging ###
logFormatStr = "[%(asctime)s] " \
               "p%(process)s {%(pathname)s:%(lineno)d}" \
               " %(levelname)s - %(message)s"
logging.basicConfig(
    format=logFormatStr,
    filename="global.log",
    level=logging.DEBUG
)
formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
fileHandler = logging.FileHandler("summary.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)
app.logger.info("Logging is set up.")
print("App is setup and running on:  {0}:{1}".format(
    app.config['HOST'], app.config['PORT']))


# Add a default route for index
@app.route('/', methods=['GET'])
def index():

    num_quotes = Quotes.query.order_by(Quotes.id.asc()).count()
    r = random.randint(0, num_quotes)
    q = Quotes.query.filter_by(id=r).first_or_404()
    print(q.serialize)
    char = q.character
    quote = {'quote': q.quote_text,
             'character': f'{char.lower()}.jpg'}
    return render_template('index.html', quote=quote)


if __name__ == '__main__':
    app.run()
