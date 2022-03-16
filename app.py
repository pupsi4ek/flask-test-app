from datetime import datetime

from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret key'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id


@app.route('/')
def index():
    books = Books.query.order_by(Books.date.desc()).all()
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
