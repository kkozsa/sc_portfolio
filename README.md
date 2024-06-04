## S&C Portfolio Information System:

S&C Portfolio Information System is a web based application for users to manage their financial portfolio. 
Users can register, login, add/remove assets they interested in and monitor those assets price in realtime.
In future version users will be able to add purchase/sell data including: asset purchase date, asset price on purchased date, asset quantity, 
asset sell date, asset price on sell date. Tax calculations will be also implemented based on purchase / sell price.

## Features:

User authentication (login, register, logout)
Update user profile information
Real-time stock updates using Yahoo Finance API
Add / remove stocks on portfolio
View individual stock performance

## Users:

Registered users can create account using email and password. The registration of an admin user is not yet implemented in this version of the information system.

## Data Requirements:

For user registration, email and password required. Users can update their profile page with full name, date of birth, phone number and address. Information about assets can be added by the user on the portfolio page.

## Searching:
User should be able to search and add assets on the portfolio page via Yahoo finance API. 

## Entry and update:
User can add and remove assets. Asset information updated automatically every 60 seconds.

## Validation:
Email format and password match validation on Login / Register page.

## Technology used:
Frontend: HTML, CSS, Bootstrap, Javascript.

Backend: Python Flask, Javascript, MySQL.

External APIs: Alphavantage, Polygon, Yahoo Finance. 
External APIs were tested in the beginning of the project. Alphavantage (https://www.alphavantage.co/documentation/) is limited to 25 API requests per day, while Polygon (https://polygon.io/docs/stocks) is also limited to 5 API request per minute. You can find these test files in my "old api test files added" repository 21. Yahoo Finance API has 2000 API requests per hour, so I decided to implement that in the information system. 
(https://algotrading101.com/learn/yfinance-guide/, https://pypi.org/project/yfinance/)


## SQL code:

CREATE TABLE `users` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `full_name` varchar(45) DEFAULT NULL,
  `date_of_birth` datetime DEFAULT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `ticker` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`userid`)

CREATE TABLE `user_portfolio` (
  `userid` int DEFAULT NULL,
  `portfolio_id` int NOT NULL,
  `ticker` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`portfolio_id`),
  KEY `userid_idx` (`userid`),
  CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)

