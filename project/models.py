from sqlalchemy.orm import reconstructor

from project import db
from project.config import basedir
from project.utils import markdown_to_html


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    title = db.Column(db.String())
    category = db.Column(db.String())
    markdown = db.Column(db.String())

    def __init__(self, filename, markdown):
        self.filename = filename
        self.title = self.extract_title(filename)
        self.markdown = markdown
        self.category = self.category_from_filename(filename) or 'General'

    def update(self, new_content):
        new_html = markdown_to_html(new_content)

        with open(f'{basedir}/templates/{self.template_file}', 'w') as out:
            out.write(new_html)

        self.markdown = new_content


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

        if new_title.endswith('.md'):
            new_title = new_title[:-3]
        new_title = new_title.replace('-', ' ').replace('_', ' ')
        new_title = new_title.title()

        return new_title

    @staticmethod
    def category_from_filename(filename):
        if '/' in filename:
            return filename.split('/')[0]

        return None
