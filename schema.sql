CREATE DATABASE IF NOT EXISTS vacc_pred;
USE vacc_pred;

DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS user_inputs;

CREATE TABLE user_inputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    v012 INT,
    v106 INT,
    v190 INT,
    v025 INT,
    v101 VARCHAR(100),
    b19 INT,
    b4 INT,
    bord INT,
    h0 INT DEFAULT 0,
    h3 INT DEFAULT 0,
    h4 INT DEFAULT 0,
    h5 INT DEFAULT 0,
    h6 INT DEFAULT 0,
    h7 INT DEFAULT 0,
    h8 INT DEFAULT 0,
    h9 INT DEFAULT 0,
    h9a INT DEFAULT 0,
    h51 INT DEFAULT 0,
    h52 INT DEFAULT 0,
    h53 INT DEFAULT 0,
    h57 INT DEFAULT 0,
    h58 INT DEFAULT 0,
    h59 INT DEFAULT 0,
    h61 INT DEFAULT 0,
    h62 INT DEFAULT 0,
    h63 INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vaccine_name VARCHAR(50) NOT NULL,
    miss_probability FLOAT NOT NULL,
    risk_level ENUM('LOW','MEDIUM','HIGH') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_inputs(id) ON DELETE CASCADE
);
