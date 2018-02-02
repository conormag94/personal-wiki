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

    def __init__(self, title, markdown):
        self.title = self.extract_title(title)
        self.markdown = markdown
        self.category = self.category_from_title(title) or 'General'

    @reconstructor
    def init_template_file(self):
        """After creation, write this Note's content to its template file, notes/<id>.html"""
        template_file = f'{basedir}/templates/notes/{str(self.id)}.html'
        html = markdown_to_html(self.markdown)

        with open(template_file, 'w') as out:
            out.write(html)

        self.template_file = f'notes/{str(self.id)}.html'

    @staticmethod
    def extract_title(filename):

        new_title = filename

        if '/' in new_title:
            new_title = new_title.split('/')[-1]

        new_title = new_title.strip('.md')
        new_title = new_title.replace('-', ' ').replace('_', ' ')
        new_title = new_title.title()

        return new_title

    @staticmethod
    def category_from_title(title):
        if '/' in title:
            return title.split('/')[0]

        return None
