from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, Date, DateTime, Float, PickleType
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base
from sqlalchemy.ext.mutable import MutableDict


polygon_categories = Table('polygon_categories', Base.metadata,
    Column('polygon_id', Integer, ForeignKey('polygons.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    scoring_industrial = Column(Integer)
    scoring_f_b = Column(Integer)
    scoring_amenities = Column(Integer)
    matching_code = Column(String(500))

    polygons = relationship('Polygon', secondary=polygon_categories, back_populates='categories')

    def __init__(self, name=None):
        self.name = name


class Polygon(Base):
    __tablename__ = 'polygons'
    id = Column(Integer, primary_key=True)
    latitude_1 = Column(Float)
    longtitude_1 = Column(Float)

    latitude_2 = Column(Float)
    longtitude_2 = Column(Float)

    latitude_3 = Column(Float)
    longtitude_3 = Column(Float)

    latitude_4 = Column(Float)
    longtitude_4 = Column(Float)

    scoring_industrial = Column(Integer)
    scoring_f_b = Column(Integer)
    scoring_amenities = Column(Integer)

    categories = relationship('Categories', secondary=polygon_categories, back_populates='polygons')






