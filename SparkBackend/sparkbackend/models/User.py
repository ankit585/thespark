from sqlalchemy import Column, Integer, String,DateTime,Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker
import datetime
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    permissions = Column(Integer)
    email_verified = Column(Boolean)
    userID = Column(String(50),unique=True)
    password = Column(String(255))
    email = Column(String(255),unique=True)
    createdOn = Column(DateTime,default=datetime.datetime.now())

    def __init__(self, userID, password, email):
        """Constructor"""
        self.permissions = 0
        self.email_verified = False
        self.userID = userID
        self.password = password
        self.email = email
     

    def __repr__(self):
        return "<User('%s', '%s' , '%s', '%d', '%d','%s')>" % (self.userID,self.password,self.email,self.permissions,self.email_verified,self.createdOn)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'userID'     : self.userID,
           'password'     : self.password,
           'email'     : self.email,
           'permissions' : self.permissions,
           'email_verified'     : self.email_verified,
           'createdOn'     : self.createdOn
       }


engine = create_engine(
                "mysql://spark:pass@96.126.100.154/spark",
                isolation_level="READ UNCOMMITTED"
            )



# get a handle on the table object
users_table = User.__table__
# get a handle on the metadata
metadata = Base.metadata
metadata.create_all(engine)
