from flask import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


class AddProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    description = TextAreaField("Project Description & Features", validators=[DataRequired()])
    img_url = URLField('Image URL', validators=[DataRequired(), URL()])
    github_url = URLField('GitHub URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Project')