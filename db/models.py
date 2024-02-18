from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, text, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT as MEDIUMTEXT, LONGTEXT as LongText
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta


Base = declarative_base()

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    name_short = Column(String(100))
    location = Column(String(500))
    phone_number = Column(String(250))
    email = Column(String(250))
    description = Column(LongText)
    image = Column(LongText)   
    website = Column(String(500))
    facebook = Column(String(500))
    twitter = Column(String(500))
    instagram = Column(String(500))
    youtube = Column(String(500))
    events = relationship('Event', back_populates='organization')
    prayer_times = relationship('PrayerTime', back_populates='organization')

    def __repr__(self):
        return f'<Organization {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_short': self.name_short,
            'location': self.location,
            'phone_number': self.phone_number,
            'email': self.email,
            'description': self.description,
            'image': self.image,
            'website': self.website,
            'facebook': self.facebook,
            'twitter': self.twitter,
            'instagram': self.instagram,
            'youtube': self.youtube
        }

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    link = Column(Text)
    sub_links = Column(Text)
    image = Column(LongText)
    date = Column(DateTime)
    start_time = Column(String(50))
    end_time = Column(String(50))
    location = Column(String(500))
    short_description = Column(Text)
    full_description = Column(MEDIUMTEXT)
    other_info = Column(MEDIUMTEXT)
    cost = Column(String(100))
    category = Column(String(250))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='events')

    def __repr__(self):
        return f'<Event {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'link': self.link,
            'sub_links': self.sub_links,
            'image': self.image,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'short_description': self.short_description,
            'full_description': self.full_description,
            'other_info': self.other_info,
            'cost': self.cost,
            'category': self.category,
            'created_at': self.created_at,
            'organization_id': self.organization_id

        }

class PrayerTime(Base):
    __tablename__ = 'prayer_times'
    id = Column(Integer, primary_key=True)
    prayer_name = Column(String(50), nullable=False)
    athan_time = Column(String(50), nullable=False)
    iqama_time = Column(String(50))
    jumuah_time = Column(String(50))
    jumuah_time2 = Column(String(50))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='prayer_times')

    def __repr__(self):
        return f'<PrayerTime {self.prayer_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'prayer_name': self.prayer_name,
            'athan_time': self.athan_time,
            'iqama_time': self.iqama_time,
            'jumuah_time': self.jumuah_time,
            'jumuah_time2': self.jumuah_time2,
            'created_at': self.created_at,
            'organization_id': self.organization_id
        }

class Database:
    def __init__(self, username, password, host, port, database_name):
        self.engine = create_engine(
            f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}',
            echo=True,  # Set to False in production
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def close_connection(self):
        self.engine.dispose()

    def add_organization(self, id, name, name_short, location=None, phone_number=None, email=None, description=None, website=None, facebook=None, twitter=None, instagram=None, youtube=None, image=None):
        session = self.Session()

        existing_organization = session.query(Organization).filter(Organization.name == name).first()

        if not existing_organization:
            new_organization = Organization(name=name, name_short=name_short, location=location, phone_number=phone_number, email=email, description=description, website=website, facebook=facebook, twitter=twitter, instagram=instagram, youtube=youtube, image=image)
            session.add(new_organization)
            session.commit()
        session.close()

    def add_event(self, title=None, date=None, image=None, link=None, start_time=None, end_time=None, location=None, 
                  short_description=None, full_description=None, category=None, organization_id=None, sub_links=None, other_info=None, created_at=None, cost=None):
        session = self.Session()

        # check if title is null or empty
        # Check if the event already exists in the database by checking the title and organization_id however if title is null or empty then check by image and organization_id. If it exists, update the existing entry, otherwise add a new entry
        # existing_event = session.query(Event).filter( (Event.title == title and Event.organization_id == organization_id) or (Event.image == image and Event.organization_id == organization_id) ).first()
        if title is None or title == "":
            existing_event = session.query(Event).filter(Event.image == image, Event.organization_id == organization_id).first()
        else:
            existing_event = session.query(Event).filter(Event.title == title, Event.organization_id == organization_id).first()

        if not existing_event:
            new_event = Event(title=title, date=date, start_time=start_time, end_time=end_time,
                            location=location, link=link, image=image,
                            short_description=short_description, full_description=full_description,
                            category=category, organization_id=organization_id, created_at=created_at, sub_links=sub_links, other_info=other_info, cost=cost)
            session.add(new_event)
            session.commit()
        else:
            existing_event.title = title
            existing_event.date = date
            existing_event.start_time = start_time
            existing_event.end_time = end_time
            existing_event.location = location
            existing_event.link = link
            existing_event.image = image
            existing_event.short_description = short_description
            existing_event.full_description = full_description
            existing_event.category = category
            existing_event.organization_id = organization_id
            existing_event.created_at = created_at
            existing_event.sub_links = sub_links
            existing_event.other_info = other_info
            existing_event.cost = cost
            session.commit()
        session.close()

    def add_prayer_time(self, prayer_name, athan_time, iqama_time=None, jumuah_time=None, jumuah_time2=None, organization_id=None):
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
                existing_prayer_time.jumuah_time2 = jumuah_time2
                session.commit()
                break

        else:
            # If the loop completes without a break, it means no existing entry has been updated,
            # so add a new prayer time
            new_prayer_time = PrayerTime(prayer_name=prayer_name, athan_time=athan_time,
                                         iqama_time=iqama_time, jumuah_time=jumuah_time, jumuah_time2=jumuah_time2, organization_id=organization_id)
            
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
    
    def get_all_organizations(self):
        session = self.Session()
        organizations = session.query(Organization).all()
        organizations = [organization.to_dict() for organization in organizations]
        session.close()
        return organizations
    
    def get_all_events(self):
        session = self.Session()
        events = session.query(Event).all()
        session.close()
        return events
    
    def get_all_events_created_today(self):
        session = self.Session()

        # Get the current date and time
        now = datetime.now()
        # Create datetime objects representing the start and end of the current day
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1, seconds=-1)
        # Filter events created between the start and end of the current day
        events = session.query(Event).filter(Event.created_at >= start_of_day, Event.created_at <= end_of_day).all()
        # Convert the events to dictionaries
        events = [event.to_dict() for event in events]
        session.close()
        return events
    
    def get_all_prayer_times(self):
        session = self.Session()
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1, seconds=-1)
        prayer_times = session.query(PrayerTime).filter(PrayerTime.created_at >= start_of_day, PrayerTime.created_at <= end_of_day).all()
        prayer_times = [prayer_time.to_dict() for prayer_time in prayer_times]
        session.close()
        return prayer_times
    
    def get_all_events_by_organization_today(self, organization_id):
        session = self.Session()
        # get all events by organization id and created today
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1, seconds=-1)
        events = session.query(Event).filter(Event.organization_id == organization_id, Event.created_at >= start_of_day, Event.created_at <= end_of_day).all()
        events = [event.to_dict() for event in events]
        session.close()
        return events
    
    def get_all_prayer_times_by_organization(self, organization_id):
        session = self.Session()
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1, seconds=-1)
        prayer_times = session.query(PrayerTime).filter(PrayerTime.organization_id == organization_id, PrayerTime.created_at >= start_of_day, PrayerTime.created_at <= end_of_day).all()
        prayer_times = [prayer_time.to_dict() for prayer_time in prayer_times]
        session.close()
        return prayer_times
    
    def get_all_events_by_date(self, date):
        session = self.Session()
        events = session.query(Event).filter(Event.date == date).all()
        session.close()
        return events
    
    def get_all_events_by_organization_name(self, organization_name):
        session = self.Session()
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1, seconds=-1)
        events = session.query(Event).join(Organization).filter(Organization.name_short == organization_name, Event.created_at >= start_of_day, Event.created_at <= end_of_day).all()
        events = [event.to_dict() for event in events]
        session.close()
        return events
    
    def get_all_prayer_times_by_organization_name(self, organization_name):
        session = self.Session()
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        end_of_day = start_of_day + timedelta(days=1, seconds=-1)
        prayer_times = session.query(PrayerTime).join(Organization).filter(Organization.name_short == organization_name, PrayerTime.created_at >= start_of_day, PrayerTime.created_at <= end_of_day).all()
        prayer_times = [prayer_time.to_dict() for prayer_time in prayer_times]
        session.close()
        return prayer_times
    
