from sqlalchemy import (create_engine, ForeignKey, Column, Integer, String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine('sqlite:///playlist.db')
Base = declarative_base()


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    artist = Column(String())
    year = Column(Integer(), default = '')
    yt_link = Column(String())

    streams = relationship('Stream', backref=backref('song'), cascade='all, delete')
    listeners = association_proxy('streams', 'listener', creator=lambda li: Stream(listener=li))

    def __repr__(self):
        return f'{self.name} by {self.artist}'
    


class Listener(Base):
    __tablename__ = 'listeners'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), unique=True)
    age = Column(Integer())
    
    streams = relationship('Stream', backref=backref('listener'), cascade='all, delete')
    songs = association_proxy('streams', 'song', creator=lambda sn: Stream(song=sn))

    def __repr__(self):
        return f'Listener {self.id}: {self.name}, {self.age}'



class Stream(Base):
    __tablename__ = 'streams'
    
    id = Column(Integer(), primary_key=True)
    song_name = Column(String())

    song_id = Column(Integer(), ForeignKey('songs.id'))
    listener_id = Column(Integer(), ForeignKey('listeners.id'))

    def __repr__(self):
        return f'Stream {self.id}: {self.song_name} streamed by {self.listener_id}'
