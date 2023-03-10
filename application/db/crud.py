from sqlalchemy.orm import Session
from application.db.models import Book, Author


def get_all_authors(db: Session, unknown=False):
    """Returns all authors from database
    db - Session object connected to your database
    unknown - boolean variable: True - includes Unknown author to the list, False(default) - does not include Unknown author """
    query = db.query(Author)
    if not unknown:
        query = query.filter(Author.id > 1)
    query = query.all()
    return query


def add_author(db: Session, name: str, country: str, year: int, sex: str):
    """Adds new Author entity into Author's table
    db - Session object connected to your database
    name - name of the new author
    conntry - name of the new author
    year - year of birth of the new author
    sex - sex of the new author"""
    author = Author(name=name, country=country, year=year, sex=sex)
    db.add(author)
    db.commit()
    return True


def get_all_books(db: Session):
    """Retunrs list of all books from Book's table
    db - Session object connected to your database"""
    query = db.query(Book).all()
    return query


def get_book_by_id(db: Session, book_id: int):
    """Returns single book entity from Book's table by it's id
    db - Session object connected to your database
    book_id - id of returned book"""
    query = db.query(Book).filter(Book.id == book_id).one()
    return query


def get_author_by_id(db: Session, author_id: int):
    """Returns single author entity from Author's table by it's id
    db - Session object connected to your database
    author_id - id of returned author"""
    query = db.query(Author).filter(Author.id == author_id).one()
    return query


def delete_book_by_id(db: Session, book_id: int):
    """Deletes singe book entity from Book's table by it's id
    db - Session object connected to your database
    book_id - id of deleted book"""
    db.query(Book).filter(Book.id == book_id).delete()
    db.commit()
    return True


def delete_author_by_id(db: Session, author_id: int):
    """Deletes single author entity from Author's table by it's id, if any book in Book's table has it's author field
    referring to deleted author, it's author is changed to Unknown.
    db - Session object connected to your database
    author_id - id of deleted author"""
    db.query(Book).filter(Book.author_id == author_id).update({Book.author_id: 1})
    db.query(Author).filter(Author.id == author_id).delete()
    db.commit()
    return True


def edit_book(db: Session, book_id: int, name: str, genre: str, year: int, author_id: int):
    """Updates record of existing book in Book's table
    db - Session object connected to your database
    book_id - updated book's id
    name - book's new name
    genre - book's new genre
    year - book's new year of publishing
    author_id - book's new author"""
    db.query(Book).filter(Book.id == book_id).update(
        {Book.name: name, Book.genre: genre, Book.year: year, Book.author_id: author_id})
    db.commit()
    return True


def edit_author(db: Session, author_id: int, name: str, country: str, year: int, sex: str):
    """Updates record of existing author in Author's table
    db - Session object connected to your database
    author_id - updated author's id
    name - author's new name
    country - author's new country of origin
    year - author's new year of birth
    sex - author's new sex"""
    db.query(Author).filter(Author.id == author_id).update(
        {Author.name: name, Author.country: country, Author.year: year, Author.sex: sex})
    db.commit()
    return True


def add_book(db: Session, name: str, genre: str, year: int, author_id: int):
    """Adds new author entity to Author's table
    db - Session object connected to your database
    name - new book's name
    genre - new book's genre
    year - new book's year of publishing
    author_id - new book's author"""
    book = Book(name=name, genre=genre, year=year, author_id=author_id)
    db.add(book)
    db.commit()
    return True


if __name__ == '__main__':
    from application.db import Session, engine

    Session.configure(bind=engine)
    session = Session()
    add_author(session, 'Unknown', 'Unknown', 0, 'Unknown')
