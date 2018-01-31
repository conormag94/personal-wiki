from sqlalchemy.orm import reconstructor

from project import db
from project.config import basedir
from project.utils import markdown_to_html


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    category = db.Column(db.String())
    markdown = db.Column(db.String())

    def __init__(self, title, markdown, category='General'):
        self.title = title
        self.markdown = markdown
        self.category = category

    @reconstructor
    def init_template_file(self):
        """After creation, write this Note's content to its template file, notes/<id>.html"""
        template_file = f'{basedir}/templates/notes/{str(self.id)}.html'
        html = markdown_to_html(self.markdown)

        with open(template_file, 'w') as out:
            out.write(html)

        self.template_file = f'notes/{str(self.id)}.html'
