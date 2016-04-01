import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import backref, relationship

from tuneful import app
from .database import Base, engine


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    file_ = relationship(File, backref=backref('song', uselist=False))

    def as_dict(self):
        return {
            'id': self.id,
            'file': {
                'id': self.file_.id,
                'name': self.file_.name
            }
        }
