import pytest
from flask import url_for
from application.db.models import Author, Book, Base
from application.db import Session


@pytest.fixture()
def app():
    from application.routes import app
    from sqlalchemy import create_engine

    app.config.from_object('application.config.TestingConfig')
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.bind = engine
    Session.configure(bind=engine)
    session = Session()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with app.app_context():
        authors = [Author(id=1, name='test_author1', country='test_country1', year=1900, sex='Male'),
                   Author(id=2, name='test_author2', country='test_country2', year=1902, sex='Female')]
        books = [Book(id=1, name='test_book1', genre='test_genre1', year=1201, author_id=1),
                 Book(id=2, name='test_book2', genre='test_genre2', year=1202, author_id=2),
                 Book(id=3, name='test_book3', genre='test_genre3', year=1203, author_id=2)]
        session.add_all(authors)
        session.commit()
        session.add_all(books)
        session.commit()
    yield app


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def ctx(app):
    with app.test_request_context() as context:
        yield context


def test_books(client, ctx):
    url = url_for('books')
    response = client.get(url)
    assert response.status_code == 200

    data = response.data.decode('utf-8')
    assert 'test_book1' in data
    assert 'test_book2' in data
    assert 'test_book3' in data
    assert 'test_book4' not in data
    assert 'test_author1' in data
    assert 'test_author2' in data
    assert 'test_genre2' in data
    assert '1202' in data
    assert '1500' not in data


def test_add_book(client, ctx):
    url = url_for('add_book')
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, data={'name': 'test_book4', 'genre': 'test_genre4', 'year': '1204', 'author_id': '1'})
    assert response.status_code == 302
    url = url_for('books')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_book4' in data
    assert '1204' in data


def test_edit_book(client, ctx):
    url = url_for('edit_book', book_id=2)
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, data={'name': 'test_book2_edited', 'genre': 'test_genre2_edited', 'year': '1205',
                                      'author_id': '1'})
    assert response.status_code == 302
    url = url_for('books')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_book2_edited' in data
    assert '1205' in data


def test_delete_book(client, ctx):
    url = url_for('delete_book', book_id=2)
    response = client.get(url)
    assert response.status_code == 302
    url = url_for('books')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_book2' not in data
    assert '1202' not in data


def test_authors(client, ctx):
    url = url_for('authors')
    response = client.get(url)
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert 'test_author2' in data
    assert 'Female' in data
    assert 'test_country2' in data
    assert '1902' in data


def test_add_author(client, ctx):
    url = url_for('add_author')
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, data={'name': 'test_author3', 'country': 'test_country3', 'year': '1903', 'sex': 'Male'})
    assert response.status_code == 302
    url = url_for('authors')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_author3' in data
    assert 'test_country3' in data
    assert '1903' in data


def test_edit_author(client, ctx):
    url = url_for('edit_author', author_id=2)
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, data={'name': 'test_author2_edited', 'country': 'test_country2_edited', 'year': '1905', 'sex': 'Male'})
    assert response.status_code == 302
    url = url_for('authors')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_author2_edited' in data
    assert 'test_country2_edited' in data
    assert '1905' in data


def test_delete_author(client, ctx):
    url = url_for('delete_author', author_id=2)
    response = client.get(url)
    assert response.status_code == 302
    url = url_for('authors')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_author2' not in data
    assert 'test_country2' not in data
    url = url_for('books')
    response = client.get(url)
    data = response.data.decode('utf-8')
    assert 'test_author2' not in data
