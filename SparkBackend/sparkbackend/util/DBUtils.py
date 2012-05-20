from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sparkbackend.util.Callable import Callable

class DBUtils():
    def getSession():
      engine = create_engine(
                "mysql://spark:pass@96.126.100.154/spark",
                isolation_level="READ UNCOMMITTED"
            )
      Session = sessionmaker(bind=engine)
      return  Session()

    getSession = Callable(getSession)

