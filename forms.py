from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField("What's the title?", validators=[DataRequired()])
    genre = SelectField('Genre: ', coerce=int, validators=[DataRequired()])
    author = StringField("Author: ", validators=[DataRequired()])
    description = TextAreaField('Description: ', validators=[DataRequired()])
    submit = SubmitField('Save')


class GenreForm(FlaskForm):
    name = StringField("Name of genre? ", validators=[DataRequired()])
    submit = SubmitField('Add')


class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Search')