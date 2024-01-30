# This is a script to populate the org table with the data from the orgs.csv in the data folder file using the ORM

import csv
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Organization
import logging

# create a database connection
engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# open the csv file
with open('data/orgs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # create an organization object
        org = Organization(
            name=row['name'],
            location=row['location'],
            phone_number=row['phone_number'],
            email=row['email'],
            website=row['website'],
            facebook=row['facebook'],
            twitter=row['twitter'],
            instagram=row['instagram'],
            youtube=row['youtube']
        )
        # add the organization object to the database
        session.add(org)
        session.commit()
        logging.info(f'Added {org.name} to the database')
    logging.info('All organizations added to the database')
    session.close()
    logging.info('Database connection closed')

