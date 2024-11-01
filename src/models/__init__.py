#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



engine = create_engine("mysql+pymysql://root@localhost/ceamovildb2")
connection = engine.connect()

Base = declarative_base()
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

session = Session()






