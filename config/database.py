import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  #To manipulate tables

#Name of the database and route
sqlite_file_name = '../database.sqlite'  

#Read the current loc of this file
base_dir = os.path.dirname(os.path.realpath(__file__))

#Create url for the data base
database_url = f'sqlite:///{os.path.join(base_dir, sqlite_file_name)}'

#the engine of the data base
engine = create_engine(database_url, echo=True)

#Create the session to connect to the data base
Session = sessionmaker(bind=engine)

#instance to manage the tables
Base = declarative_base()