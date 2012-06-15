from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker
import datetime
Base = declarative_base()

########################################################################
class EmailCode(Base):
    """"""
    __tablename__ = "email_code"

    userKey = Column(Integer, primary_key=True)
    userKey = Column(Integer,unique=True)
    code = Column(String(255),unique=True)

    def __init__(self, userKey, code):
        """Constructor"""
        self.userKey = userKey
        self.code = code
     

    def __repr__(self):
        return "<EmailCode('%d', '%s')>" % (self.userKey,self.code)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'userKey'     : self.userKey,
           'code'     : self.code
       }


engine = create_engine(
                "mysql://spark:pass@96.126.100.154/spark",
                isolation_level="READ UNCOMMITTED"
            )



# get a handle on the table object
email_code_table = EmailCode.__table__
# get a handle on the metadata
metadata = Base.metadata
metadata.create_all(engine)
