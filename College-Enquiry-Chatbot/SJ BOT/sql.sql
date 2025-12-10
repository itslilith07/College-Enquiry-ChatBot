CREATE DATABASE register;

USE register;

CREATE TABLE users (
    name VARCHAR(30),
    email VARCHAR(30),
    password VARCHAR(15)
);

CREATE TABLE suggestion (
    email VARCHAR(30),
    message VARCHAR(255)
);
