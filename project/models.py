from sqlalchemy.orm import reconstructor

from project import db


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    category = db.Column(db.String())

    @reconstructor
    def init_template_file(self):
        """After creation, set the name of this Note's template file, notes/<id>.html"""
        self.template_file = f'notes/{str(self.id)}.html'
