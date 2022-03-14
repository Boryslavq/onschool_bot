from sqlalchemy import Column, create_engine, Integer, Unicode, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from data import config


class ConnectDB:
    def __init__(self):
        super(ConnectDB, self).__init__()
        self.engine = create_engine(config.sqlite_uri)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()
        self.session = self.Session()

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)


db = ConnectDB()


class Users(db.Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    fullname = Column(Unicode)
    id = relationship('Bills', backref='users')


class Bills(db.Base):
    __tablename__ = 'bills'
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, primary_key=True)
    gmail = Column(Unicode)
    full_name = Column(Unicode)
    phone = Column(Unicode, nullable=True)
    price = Column(Integer)
    bill_id = Column(Integer, nullable=True)


def create_db():
    db.create_tables()
