from sqlalchemy import Column, Integer, String,DateTime,Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker
import datetime
Base = declarative_base()

########################################################################
class UserProfile(Base):
    """Table to store user profile"""
    __tablename__ = "user_profiles"

    userKey = Column(Integer, primary_key=True)
    city = Column(String(64))
    state = Column(String(64))
    country = Column(String(32))
    dob = Column(DateTime)
    createdOn = Column(DateTime,default=datetime.datetime.now())

    def __init__(self, userKey,city,state,country,dob):
        """Constructor"""
        self.userKey = userKey
        self.city = city
        self.state = state
        self.country = country
        self.dob = dob
     

    def __repr__(self):
        return "<UserProfile('%d', '%s' , '%s','%s','%s')>" % (self.userKey,self.city,self.state,self.country,self.dob)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'userKey'     : self.userKey,
           'city'     : self.city,
           'state'     : self.state,
           'country'     : self.dob
       }


engine = create_engine(
                "mysql://spark:pass@96.126.100.154/spark",
                isolation_level="READ UNCOMMITTED"
            )



# get a handle on the table object
user_profiles_table = UserProfile.__table__
# get a handle on the metadata
metadata = Base.metadata
metadata.create_all(engine)
