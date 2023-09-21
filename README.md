F1 Connect 

A social media application for Formuala 1 Racing fans to connect with teams and each other. Fans can connect with each other and follow their favorite teams. The application notifies users when a race has begun and tells them the results post race. They can also view historic race information. 

To setup Database:

1 - Create the database executing CREATE DATABASE project in sql shell

2- install psycopg2-binary package in virtual environment -> can be done using pip install

3- execute the commands

export DB_USERNAME="" -> enter the username for your sql profile within the quotation marks
export DB_PASSWORD="" -> enter password for sql profile within the quotation marks
4 - run the init_db.py file -> python init_db.py

This sets up the database on your local machine for data be added and removed

Then run main.py.