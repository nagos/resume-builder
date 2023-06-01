DROP DATABASE IF EXISTS resume;
CREATE DATABASE resume;
USE resume;
CREATE TABLE users (
    id int NOT NULL AUTO_INCREMENT, 
    login varchar(255) UNIQUE NOT NULL, 
    password varchar(255) NOT NULL, 
    PRIMARY KEY(id)
);
CREATE TABLE resume (
    id int NOT NULL AUTO_INCREMENT, 
    user_id int NOT NULL, 
    title varchar(255) NOT NULL, 
    text TEXT,
    PRIMARY KEY(id), 
    FOREIGN KEY (user_id) REFERENCES users (id)
);
