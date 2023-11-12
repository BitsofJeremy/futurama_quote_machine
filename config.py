import os

# hard set to not use DB
ENV = 'development'
APP_NAME = 'futurama_quote_machine'

if ENV == 'development':
    # We are in dev
    HOST = '127.0.0.1'
    PORT = '5000'
    # SQLite DB info
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'futurama_quote_machine.db')

    # this is the user lookup DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

else:
    # We are prod
    HOST = '127.0.0.1'
    PORT = '5000'
    # Connect to MariaDB
    DBHOST = ''
    DBNAME = ''
    DBUSER = ''
    DBPASSWORD = ''

