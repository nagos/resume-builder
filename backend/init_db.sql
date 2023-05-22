CREATE DATABASE resume;
USE resume;
CREATE TABLE users (id int NOT NULL AUTO_INCREMENT, login varchar(255) UNIQUE, password varchar(255), PRIMARY KEY(id));
