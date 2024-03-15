DROP DATABASE IF EXISTS banking_system;
CREATE DATABASE banking_system;
USE banking_system;

CREATE DATABASE banking_system;
USE banking_system;

CREATE TABLE Users (
	id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(191) NULL DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Accounts (
	id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    account_type VARCHAR(255) NOT NULL,
    account_number VARCHAR(255) UNIQUE NOT NULL,
    balance DECIMAL(10,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Transactions(
	id INT PRIMARY KEY  AUTO_INCREMENT, 
    from_account_id INT,
    to_account_id INT,
    amount DECIMAL(10,2),
    type VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES Accounts(id),
    FOREIGN KEY (to_account_id) REFERENCES Accounts(id)
);

SELECT * FROM Users
SELECT * FROM Accounts
SELECT * FROM Transactions