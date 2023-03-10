from application import app
from sqlalchemy import create_engine
from flask import render_template, request, redirect, url_for
from application.db import Session, crud

genres = ['fantasy', 'sci-fi', 'comedy', 'drama']

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session.configure(bind=engine)
session = Session()

@app.route('/')
@app.route('/books')
def books():
    return render_template('Books.html', all_books=crud.get_all_books(session))


@app.route('/authors')
def authors():
    return render_template('Authors.html', all_authors=crud.get_all_authors(session))


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    name = request.form.get('name')
    country = request.form.get('country')
    year = request.form.get('year')
    sex = request.form.get('sex')
    if name:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = 0
        crud.add_author(session, name, country, year, sex)
        return redirect(url_for('authors'))
    return render_template('add_author.html')


@app.route('/edit_author', methods=['GET', 'POST'])
def edit_author():
    author_id = int(request.args.get('author_id'))
    author = crud.get_author_by_id(session, author_id)
    name = request.form.get('name')
    country = request.form.get('country')
    year = request.form.get('year')
    sex = request.form.get('sex')
    if name:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = 0
        crud.edit_author(session, author_id, name, country, year, sex)
        return redirect(url_for('authors'))
    return render_template('edit_author.html', author=author)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    name = request.form.get('name')
    year = request.form.get('year')
    author_id = request.form.get('author_id')
    if name:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = 0
        genre = ""
        for gen in genres:
            try:
                genre += request.form.get(gen) + ', '
            except TypeError:
                pass
        if genre == '':
            genre = 'None'
        else:
            genre = genre[:-2]
        crud.add_book(session, name, genre, year, int(author_id))
        return redirect(url_for('books'))
    return render_template('add_book.html', authors=crud.get_all_authors(session, unknown=True), genres=genres)


@app.route('/edit_book', methods=['GET', 'POST'])
def edit_book():
    book_id = int(request.args.get('book_id'))
    book = crud.get_book_by_id(session, book_id)
    name = request.form.get('name')
    year = request.form.get('year')
    author_id = request.form.get('author_id')
    if name:
        try:
            year = int(year)
        except (TypeError, ValueError):
            year = 0
        genre = ""
        for gen in genres:
            try:
                genre += request.form.get(gen) + ', '
            except TypeError:
                pass
        if genre == '':
            genre = 'None'
        else:
            genre = genre[:-2]
        crud.edit_book(session, book_id=book_id, name=name, genre=genre, year=year, author_id=int(author_id))
        return redirect(url_for('books'))
    return render_template('edit_book.html', book=book, authors=crud.get_all_authors(session, unknown=True),
                           genres=genres)


@app.route('/delete_book')
def delete_book():
    book_id = int(request.args.get('book_id'))
    crud.delete_book_by_id(session, book_id)
    return redirect(url_for('books'))


@app.route('/delete_author')
def delete_author():
    author_id = int(request.args.get('author_id'))
    crud.delete_author_by_id(session, author_id)
    return redirect(url_for('authors'))




