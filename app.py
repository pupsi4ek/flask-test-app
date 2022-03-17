from datetime import datetime

from flask import Flask, render_template, redirect, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import BookForm, GenreForm, SearchForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id


class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Books', backref='genres', lazy=True)

    def __repr__(self):
        return '<%r genre>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    books = Books.query.order_by(Books.date.desc()).all()
    genres = Genres.query.all()
    book_select = request.args.get('book_select') == 'true'

    q = request.args.get('q')
    if q:
        books = Books.query.filter(Books.title.contains(q) | Books.genre.contains(q) |
                                   Books.author.contains(q) | Books.date.contains(q)).order_by(Books.date.desc())

    return render_template('index.html', books=books, genres=genres, book_select=book_select)


@app.route('/create-book', methods=['GET', 'POST'])
def createBook():
    title = None
    description = None
    author = None
    form = BookForm()
    form.genre.choices = [(g.id, g.name) for g in Genres.query.order_by('name')]

    if form.validate_on_submit():
        title = Books.query.filter_by(title=form.title.data).first()
        if title is None:
            book = Books(title=form.title.data, genre=form.genre.data, author=form.author.data,
                         description=form.description.data)
            try:
                db.session.add(book)
                db.session.commit()
                form.title.data = ''
                form.genre.data = ''
                form.description.data = ''
                form.author.data = ''
                flash('Book added successfully!')
                return redirect('/')
            except:
                return "It's an error occurred while trying to create book"
        else:
            flash('Book already exists!')

    return render_template('create-book.html', title=title, form=form)


@app.route('/<int:id>')
def book_info(id):
    book = Books.query.get_or_404(id)
    genres = Genres.query.all()
    return render_template('book_info.html', book=book, genres=genres)


@app.route('/<int:id>/delete')
def book_delete(id):
    book = Books.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!')
        return redirect('/')
    except:
        return "It's an error occurred while trying to delete book"


@app.route('/<int:id>/update', methods=['GET', 'POST'])
def book_update(id):
    book = db.session.query(Books).get_or_404(id)
    form = BookForm(obj=book)
    form.genre.choices = [(g.id, g.name) for g in Genres.query.order_by('name')]
    if form.validate_on_submit():
        try:
            form.populate_obj(book)
            db.session.add(book)
            db.session.commit()
            flash('Book updated successfully')
            return redirect('/')
        except:
            return "It's an error occurred while updating book"

    return render_template('book_update.html', form=form)


@app.route('/create-genre', methods=['GET', 'POST'])
def createGenre():
    name = None
    form = GenreForm()

    if form.validate_on_submit():
        name = Genres.query.filter_by(name=form.name.data).first()
        if name is None:
            genre = Genres(name=form.name.data)
            try:
                db.session.add(genre)
                db.session.commit()
                form.name.data = ''
                flash('Genre added successfully!')
                return redirect('/')
            except:
                return "It's an error occurred while trying to create genre"
        else:
            flash('Genre already exists!')

    return render_template('create-genre.html', name=name, form=form)


if __name__ == '__main__':
    app.run(debug=True)
