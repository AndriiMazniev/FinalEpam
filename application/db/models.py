from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()
Base.metadata.clear()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    country = Column(String(50))
    year = Column(Integer)
    sex = Column(String(10))


class Book(Base):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    genre = Column(String(50))
    year = Column(Integer)
    author_id = Column(ForeignKey(Author.id), nullable=False)
    author = relationship(Author)





if __name__ == '__main__':
    from application.db import engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



