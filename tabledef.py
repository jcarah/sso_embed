from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///sso.db', echo=True)
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    permissions = Column(String)
    models = Column(String)
    state = Column(String)
    external_group_id = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, username, first_name, last_name, password, permissions, models, state, external_group_id):
        """"""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.permissions = permissions
        self.models = models
        self.state = state
        self.external_group_id = external_group_id


# create tables
Base.metadata.create_all(engine)
