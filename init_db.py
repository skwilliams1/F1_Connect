import os
import psycopg2

# creating cursor connection to database. The database is located on local server
connection = psycopg2.connect(
    host = "localhost",
    database = "project",
    user = os.environ['DB_USERNAME'],
    password = os.environ['DB_PASSWORD']
)



# create cursor connection
cursor = connection.cursor()


# cursor.execute("DROP TABLE Posts;")

# Creating tables for database


cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
  Username varchar(32) PRIMARY KEY NOT NULL,
  Email varchar(30) NOT NULL,
  Password varchar(75) NOT NULL,
  Name varchar(32) NOT NULL,
  Badge varchar(10) NOT NULL,
  DateCreated Date
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Posts (
    PID SERIAL PRIMARY KEY NOT NULL,
    Likes INTEGER NULL,
    Text varchar(256) NOT NULL,
    Tags varchar(20) NULL,
    Author varchar(32) REFERENCES Users NOT NULL,
    PostCreated TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS followers (
    User1 varchar(32) NOT NULL,
    User2 varchar(32) NOT NULL,
    DayBecameFriend TIMESTAMP
);
""")

# cursor.execute('CREATE TABLE IF NOT EXISTS Official( Username VARCHAR (10) PRIMARY KEY, Name VARCHAR(30), Password VARCHAR(16), Email VARCHAR(30), Authentication VARCHAR (5));')

# cursor.execute('CREATE TABLE IF NOT EXISTS Unofficial(Username VARCHAR(10) PRIMARY KEY , Name VARCHAR(30), Password VARCHAR(16), Premium VARCHAR(5), TIMEZONE VARCHAR(30), DOB DATE);')

# cursor.execute('CREATE TABLE IF NOT EXISTS Post (PostID INTEGER PRIMARY KEY, Username VARCHAR(10) REFERENCES Official NOT NULL, Date DATE);')

# cursor.execute('CREATE TABLE IF NOT EXISTS Friends (User1 VARCHAR (30) REFERENCES unOfficial NOT NULL, User2 VARCHAR(30) REFERENCES unOfficial NOT NULL);')

# cursor.execute('CREATE TABLE IF NOT EXISTS Follow(User1 VARCHAR(30) REFERENCES Unofficial NOT NULL, User2 VARCHAR(30) REFERENCES Official NOT NULL);')

# cursor.execute('CREATE TABLE IF NOT EXISTS DriversChamps(Year DATE PRIMARY KEY, Name VARCHAR(30), Points INTEGER, Number INTEGER, Age INTEGER, Nationality VARCHAR(25));')

# cursor.execute('CREATE TABLE IF NOT EXISTS TeamChamps( Year DATE PRIMARY KEY, Name VARCHAR(30), Points INTEGER, CarModel VARCHAR(20), TeamPrinciple VARCHAR(30), Driver1 VARCHAR(30), Driver2 VARCHAR(30), LeadMechanic VARCHAR(30));')

# cursor.execute('CREATE TABLE IF NOT EXISTS Race( RaceID INTEGER PRIMARY KEY, Name VARCHAR(30), Date DATE, Location Text, StartTime TIMESTAMP(2), Winner VARCHAR(30));')

# cursor.execute('CREATE TABLE IF NOT EXISTS Notifies(RaceID INTEGER REFERENCES Race NOT NULL, Username VARCHAR(10) REFERENCES unOfficial NOT NULL, Status VARCHAR(10));')



# committing changes to databse
connection.commit()

# closing connection and cursor
cursor.close()
connection.close()