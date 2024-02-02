# This is a script to populate the org table with the data from the orgs.csv in the data folder file using the ORM
import os
import csv
from ..db.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from ..db.models import Organization, Database
import logging

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'org.csv')

# create a database connection
db = Database(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# open the csv file
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        # create an organization object
        org = Organization(
            id=row['id'],
            name=row['name'],
            location=row['location'],
            phone_number=row['phone_number'],
            email=row['email'],
            description=row['description'],  # Add this line
            website=row['website'],
            facebook=row['facebook'],
            twitter=row['twitter'],
            instagram=row['instagram'],
            youtube=row['youtube']
        )
        # add the organization object to the database
        db.add_organization(
            id=org.id,
            name=org.name,
            location=org.location,
            phone_number=org.phone_number,
            email=org.email,
            description=org.description,
            website=org.website,
            facebook=org.facebook,
            twitter=org.twitter,
            instagram=org.instagram,
            youtube=org.youtube
            )
        logging.info(f'Added {org.name} to the database')
    logging.info('All organizations added to the database')
    logging.info('Database connection closed')

