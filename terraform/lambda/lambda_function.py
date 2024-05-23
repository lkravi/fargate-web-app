import pymysql
import boto3
import os

def create_user_if_not_exists(conn, user):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM mysql.user WHERE user = %s", (user,))
    if cur.fetchone():
        print(f"User '{user}' already exists.")
    else:
        create_user_query = f"CREATE USER '{user}' IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';"
        cur.execute(create_user_query)
        print(f"User '{user}' created successfully.")

def grant_privileges(conn, user):
    cur = conn.cursor()
    grant_privileges_query = f"GRANT ALL PRIVILEGES ON bookdb.* TO '{user}';"
    cur.execute(grant_privileges_query)
    cur.execute("FLUSH PRIVILEGES;")
    print(f"Granted privileges to user '{user}' on database 'bookdb'.")

def create_table_if_not_exists(conn):
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS bookdb;")
    cur.execute("USE bookdb;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            isbn VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL
        );
    """)
    print("Database and table created successfully.")

def seed_database(conn):
    cur = conn.cursor()
    cur.execute("USE bookdb;")
    cur.execute("SELECT COUNT(*) FROM books;")
    if cur.fetchone()[0] > 0:
        print("Table 'books' already seeded.")
        return

    # Seed data
    books_data = [
        ('978-0132350884', 'Head First Java', 'Robert C. Martin'),
        ('978-0201616224', 'The Pragmatic Programmer', 'Andrew Hunt'),
        ('978-0201616225', 'Madol Duwa', 'Andrew Hunt'),
        ('978-0134685991', 'Effective Java', 'Joshua Bloch')
    ]
    cur.executemany("INSERT INTO books (isbn, title, author) VALUES (%s, %s, %s);", books_data)
    print("Data seeded successfully.")

def lambda_handler(event, context):
    ENDPOINT = os.environ['DB_ENDPOINT']
    PORT = 3306
    USER = os.environ['DB_MASTER_USER']
    PASSWORD = os.environ['DB_MASTER_PASSWORD']
    DB_USER = os.environ['DB_USER']
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT)
        create_user_if_not_exists(conn, DB_USER)
        grant_privileges(conn, DB_USER)
        create_table_if_not_exists(conn)
        seed_database(conn)
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        error_message = f"Error: {str(e)}, DB Endpoint: {ENDPOINT}, DB User: {USER}, DB Port: {PORT}"
        print(error_message)
        return {"status": "error", "message": error_message}
