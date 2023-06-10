from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from fastapiapp.db.database import Base, BaseModel
from fastapiapp.util.common import hash256


class UserInfo(Base, BaseModel):
    __tablename__ = 'UserInfo'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200))
    is_admin = Column(Boolean, default=False)
    lastlogin = Column(DateTime, default=datetime.datetime.now())

    def check_password(self, _password):
        return hash256(_password) == self.password

    def make_password(self, _password):
        self.password = hash256(_password)


class UserSession(Base, BaseModel):
    __tablename__ = 'UserSession'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('UserInfo.id'))
    token = Column(String(200))
    sess2user = relationship('UserInfo', backref='user2sess')
    time = Column(DateTime,
                  onupdate=datetime.datetime.now(),
                  default=datetime.datetime.now()
                  )
    expire_time = Column(DateTime,
                         onupdate=datetime.datetime.now() + datetime.timedelta(days=1),
                         default=datetime.datetime.now() + datetime.timedelta(days=1)
                         )
