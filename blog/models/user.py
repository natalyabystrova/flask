from sqlalchemy import Column, Integer, String, Boolean
from blog.models.database import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from blog.security import flask_bcrypt
from sqlalchemy.orm import relationship, column_property


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    is_staff = Column(Boolean, nullable=False, default=False)
    email = Column(String(255), unique=True, nullable=True, default="", server_default="")
    _password = Column(LargeBinary, nullable=True)
    author = relationship("Author", uselist=False, back_populates="user")
    username = column_property(last_name + " " + first_name)

    def __repr__(self):
        return f"<User #{self.id!r} {self.username!r}>"

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = flask_bcrypt.generate_password_hash(value)

    def validate_password(self, password) -> bool:
        return flask_bcrypt.check_password_hash(self._password, password)