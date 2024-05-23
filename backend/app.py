from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import boto3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Get environment variables
USE_LOCAL_DB = os.environ.get('USE_LOCAL_DB', 'false').lower() == 'true'
ENDPOINT = os.environ.get('MYSQL_DATABASE_HOST')
PORT = int(os.environ.get('MYSQL_DATABASE_PORT', 3306))
USER = os.environ.get('MYSQL_DATABASE_USER')
REGION = os.environ.get('AWS_REGION', 'us-east-1')
DBNAME = os.environ.get('MYSQL_DATABASE_DB', 'bookdb')
SSL_CERTIFICATE = os.environ.get('SSL_CERTIFICATE', '/app/us-east-1-bundle.pem')
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

if not ENDPOINT or not USER:
    raise ValueError("Environment variables MYSQL_DATABASE_HOST and MYSQL_DATABASE_USER must be set")

logging.debug(f"Endpoint: {ENDPOINT}")
logging.debug(f"Port: {PORT}")
logging.debug(f"User: {USER}")
logging.debug(f"Region: {REGION}")
logging.debug(f"Database Name: {DBNAME}")

if not USE_LOCAL_DB:
    session = boto3.Session()
    client = session.client('rds')

def get_db_connection():
    try:
        logging.debug(f"Endpoint: {ENDPOINT}")
        logging.debug(f"Port: {PORT}")
        logging.debug(f"User: {USER}")
        logging.debug(f"Region: {REGION}")
        logging.debug(f"Database Name: {DBNAME}")

        if USE_LOCAL_DB:
            connection = pymysql.connect(
                host=ENDPOINT,
                user=USER,
                password=os.environ.get('MYSQL_DATABASE_PASSWORD'),
                port=PORT,
                database=DBNAME
            )
        else:
            token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
            logging.debug(f"Generated Auth Token: {token}")
            connection = pymysql.connect(
                host=ENDPOINT,
                user=USER,
                password=token,
                port=PORT,
                database=DBNAME,
                ssl_ca=SSL_CERTIFICATE
            )

        logging.debug("Successfully connected to the database")
        return connection
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

@app.route('/api/books', methods=['GET'])
def get_books():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books")
            result = cursor.fetchall()
        logging.debug(f"Books retrieved: {result}")
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error retrieving books: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
