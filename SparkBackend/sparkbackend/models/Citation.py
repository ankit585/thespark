#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, mapper, relation, sessionmaker

Base = declarative_base()


########################################################################

class Citation(Base):

    """"""

    __tablename__ = 'citations'

    id = Column(Integer, primary_key=True)
    content = Column(String(50))
    url = Column(String(255))

    def __init__(self, content, url):
        """Constructor"""

        self.content = content
        self.url = url

    def __repr__(self):
        return "<Citation('%s', '%s')>" % (self.content, self.url)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        return {'id': self.id, 'content': self.content, 'url': self.url}


engine = create_engine('mysql://spark:passpass@sparkdb1.ckqwp2khkc3l.us-east-1.rds.amazonaws.com/sparkdb',
                       isolation_level='READ UNCOMMITTED')

# get a handle on the table object

citations_table = Citation.__table__

# get a handle on the metadata

metadata = Base.metadata
metadata.create_all(engine)
