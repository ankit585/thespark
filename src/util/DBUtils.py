from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import util.Callable

class DBUtils():
    def getSession():
      engine = create_engine(
                "mysql://spark:pass@96.126.100.154/spark", 
                isolation_level="READ UNCOMMITTED"
            )
      Session = sessionmaker(bind=engine)
      return  Session()
     
    getSession = util.Callable.Callable(getSession)  
 
