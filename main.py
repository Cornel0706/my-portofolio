import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import AddProjectForm
from flask_ckeditor import CKEditor, CKEditorField
from flask_basicauth import BasicAuth



app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME', 'admin')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD', 'parola_secreta') 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///projects.db')
ckeditor = CKEditor(app) 
db = SQLAlchemy(app)
basic_auth = BasicAuth(app)

#My Projects TABLE
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    github_url = db.Column(db.String(200), nullable=False)

# with app.app_context():
#     db.create_all()

#Home page route with all projects
@app.route('/')
def index():
    result = db.session.execute(db.select(Project))
    all_projects = result.scalars().all()
    return render_template('index.html', projects=all_projects)

#Project detail page route
@app.route('/project/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', project=project)

#Add new project page route
@app.route('/add', methods=['GET', 'POST'])
@basic_auth.required
def add_new_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        new_project = Project(
            title=form.title.data,
            date=form.date.data,
            description=form.description.data,
            img_url=form.img_url.data,
            github_url=form.github_url.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

#Delete project route
@app.route("/delete/<int:project_id>/<string:secret_key>")
def delete_project(project_id, secret_key):
    if secret_key == "120716corneliu": 
        project_to_delete = Project.query.get_or_404(project_id)
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return "Acces neautorizat!", 403


#App run
if __name__ == '__main__':
    app.run(debug=False)
 