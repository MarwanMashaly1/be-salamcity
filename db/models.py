from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, text, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT as MEDIUMTEXT, LONGTEXT as LongText
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    location = Column(String(500))
    phone_number = Column(String(250))
    email = Column(String(250))
    description = Column(LongText)
    website = Column(String(500))
    facebook = Column(String(500))
    twitter = Column(String(500))
    instagram = Column(String(500))
    youtube = Column(String(500))
    events = relationship('Event', back_populates='organization')
    prayer_times = relationship('PrayerTime', back_populates='organization')

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    link = Column(String(500))
    image = Column(LongText)
    date = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String(500))
    short_description = Column(String(500))
    full_description = Column(Text)
    category = Column(String(250))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='events')

class PrayerTime(Base):
    __tablename__ = 'prayer_times'
    id = Column(Integer, primary_key=True)
    prayer_name = Column(String(50), nullable=False)
    athan_time = Column(DateTime, nullable=False)
    iqama_time = Column(DateTime)
    jumuah_time = Column(DateTime)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='prayer_times')

class Database:
    def __init__(self, username, password, host, port, database_name):
        self.engine = create_engine(
            f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}',
            echo=True,  # Set to False in production
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_organization(self, id, name, location=None, phone_number=None, email=None, description=None, website=None, facebook=None, twitter=None, instagram=None, youtube=None):
        session = self.Session()

        existing_organization = session.query(Organization).filter(Organization.name == name).first()

        if not existing_organization:
            new_organization = Organization(name=name, location=location, phone_number=phone_number, email=email, description=description, website=website, facebook=facebook, twitter=twitter, instagram=instagram, youtube=youtube)
            session.add(new_organization)
            session.commit()
        session.close()

    def add_event(self, title=None, date=None, image=None, link=None, start_time=None, end_time=None, location=None, 
                  short_description=None, full_description=None, category=None, organization_id=None, sub_links=None, other_info=None, created_at=None):
        session = self.Session()

        # Check if the event already exists in the database by checking the title and organization_id however if title is null or empty then check by image and organization_id
        existing_event = session.query(Event).filter( (Event.title == title and Event.organization_id == organization_id) and (Event.image == image and Event.organization_id == organization_id) ).first()
        
        if not existing_event:
            new_event = Event(title=title, date=date, start_time=start_time, end_time=end_time,
                            location=location, link=link, image=image,
                            short_description=short_description, full_description=full_description,
                            category=category, organization_id=organization_id, created_at=created_at, sub_links=sub_links, other_info=other_info)
            session.add(new_event)
            session.commit()
        session.close()

    def add_prayer_time(self, prayer_name, athan_time, iqama_time=None, jumuah_time=None, organization_id=None):
        session = self.Session()

        existing_prayer_times = session.query(PrayerTime).filter(
            PrayerTime.organization_id == organization_id
        ).all()

        for existing_prayer_time in existing_prayer_times:
            if existing_prayer_time.prayer_name == prayer_name and (existing_prayer_time.athan_time != athan_time or existing_prayer_time.iqama_time != iqama_time or existing_prayer_time.jumuah_time != jumuah_time):
                # Update the existing entry
                existing_prayer_time.athan_time = athan_time
                existing_prayer_time.iqama_time = iqama_time
                existing_prayer_time.jumuah_time = jumuah_time
                session.commit()
                break

        else:
            # If the loop completes without a break, it means no existing entry has been updated,
            # so add a new prayer time
            new_prayer_time = PrayerTime(prayer_name=prayer_name, athan_time=athan_time,
                                         iqama_time=iqama_time, jumuah_time=jumuah_time, organization_id=organization_id)
            
            session.add(new_prayer_time)
            session.commit()
        session.close()
    
    def get_organization(self, organization_id):
        session = self.Session()
        organization = session.query(Organization).filter(Organization.id == organization_id).first()
        session.close()
        return organization
    
    def get_event(self, event_id):
        session = self.Session()
        event = session.query(Event).filter(Event.id == event_id).first()
        session.close()
        return event
    
    def get_event_by_title(self, title):
        session = self.Session()
        event = session.query(Event).filter(Event.title == title).first()
        session.close()
        return event
    
    def get_event_by_date(self, date):
        session = self.Session()
        event = session.query(Event).filter(Event.date == date).first()
        session.close()
        return event
    
    def get_event_by_organization(self, organization_id):
        session = self.Session()
        event = session.query(Event).filter(Event.organization_id == organization_id).first()
        session.close()
        return event
    
    def get_event_by_organization_name(self, organization_name):
        session = self.Session()
        event = session.query(Event).join(Organization).filter(Organization.name == organization_name).first()
        session.close()
        return event
    
    def get_prayer_time(self, prayer_time_id):
        session = self.Session()
        prayer_time = session.query(PrayerTime).filter(PrayerTime.id == prayer_time_id).first()
        session.close()
        return prayer_time
    
    def get_prayer_time_by_organization(self, organization_id):
        session = self.Session()
        prayer_time = session.query(PrayerTime).filter(PrayerTime.organization_id == organization_id).first()
        session.close()
        return prayer_time
    
    
    def get_all_organizations(self):
        session = self.Session()
        organizations = session.query(Organization).all()
        session.close()
        return organizations
    
    def get_all_events(self):
        session = self.Session()
        events = session.query(Event).all()
        session.close()
        return events
    
    def get_all_prayer_times(self):
        session = self.Session()
        prayer_times = session.query(PrayerTime).all()
        session.close()
        return prayer_times
    
    def get_all_events_by_organization(self, organization_id):
        session = self.Session()
        events = session.query(Event).filter(Event.organization_id == organization_id).all()
        session.close()
        return events
    
    def get_all_prayer_times_by_organization(self, organization_id):
        session = self.Session()
        prayer_times = session.query(PrayerTime).filter(PrayerTime.organization_id == organization_id).all()
        session.close()
        return prayer_times
    
    def get_all_events_by_date(self, date):
        session = self.Session()
        events = session.query(Event).filter(Event.date == date).all()
        session.close()
        return events
    
    def get_all_events_by_organization_name(self, organization_name):
        session = self.Session()
        events = session.query(Event).join(Organization).filter(Organization.name == organization_name).all()
        session.close()
        return events
    
    def get_all_prayer_times_by_organization_name(self, organization_name):
        session = self.Session()
        prayer_times = session.query(PrayerTime).join(Organization).filter(Organization.name == organization_name).all()
        session.close()
        return prayer_times
    
