# Customer Offers

## About
The memberoffers application is a Flask Application that associates customers to offers.   It utlizes a local DynamoDB server and follows a single table design (see AWS re:invent topics). It contains 2 entities: customer and offers. The entities are prefixed in the Primary Key and Sort Key.  It has a many to many relationship and that relationship also is modeled with the PK and SK using a prefix.

The table shows the single table design.

## Installation
1.  Make sure you have Docker installed.
2.  In the same directory as the docker-compose.yml, run docker-compose up 

## Configuration
1. Goto http://localhost/dbdetails
2. Click on Intialize Table
3. Click on the sample data links.
