-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS bookdb;

-- Use the database
USE bookdb;

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL
);

-- Seed data
INSERT INTO books (isbn, title, author) VALUES
('978-0132350884', 'Head First Java', 'Robert C. Martin'),
('978-0201616224', 'The Pragmatic Programmer', 'Andrew Hunt'),
('978-0201616225', 'Madol Duwa', 'Andrew Hunt'),
('978-0134685991', 'Effective Java', 'Joshua Bloch');

-- Create the user if it does not exist
CREATE USER IF NOT EXISTS 'tf_rds_user1' IDENTIFIED BY 'password';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON bookdb.* TO 'tf_rds_user1';

-- Flush privileges
FLUSH PRIVILEGES;
