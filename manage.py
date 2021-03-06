import unittest

from flask_script import Manager

from project import create_app, db
from project.models import Note
from project.utils import files_in_repo, get_file_contents, remove_all_note_templates

app = create_app()
manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    remove_all_note_templates()


@manager.command
def seed_db():
    db.session.add(Note(filename='Testing db', markdown=b'# Some Markdown\n## Some more'))
    db.session.add(Note(filename='Git/Testing db2', markdown=b'# Some more Markdown'))
    db.session.add(Note(filename='Git/another-git_note.md', markdown=b'# Some more Markdown about Git'))
    db.session.commit()

@manager.command
def update():
    note = Note.query.filter_by(id=2).first()
    note.update('Something entirely different')
    db.session.commit()

@manager.command
def reset_db():
    recreate_db()
    seed_db()


@manager.command
def init():
    filenames = files_in_repo()
    print(filenames)
    for file in filenames:
        markdown = get_file_contents(file)
        print(markdown)
        db.session.add(Note(
            filename=file,
            markdown=markdown
        ))
        db.session.commit()


@manager.command
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
