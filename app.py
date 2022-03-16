from datetime import datetime

from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from forms import BookForm, GenreForm

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
    description = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id


class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Books', backref='genres', lazy=True)

    def __repr__(self):
        return '<%r genre>' % self.name


@app.route('/')
def index():
    books = Books.query.order_by(Books.date.desc()).all()
    genres = Genres.query.order_by(Genres.name.desc()).all()
    return render_template('index.html', books=books, genres=genres)


@app.route('/create-book', methods=['GET', 'POST'])
def createBook():
    title = None
    description = None
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
