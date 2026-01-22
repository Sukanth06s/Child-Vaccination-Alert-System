CREATE DATABASE IF NOT EXISTS vacc_pred;
USE vacc_pred;

CREATE TABLE user_inputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    location VARCHAR(100),
    past_missed_vaccines INT DEFAULT 0,
    awareness_level INT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    risk_score FLOAT NOT NULL,
    alert_level ENUM('LOW','MEDIUM','HIGH') NOT NULL,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_inputs(id)
);
