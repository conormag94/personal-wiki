import unittest

from flask_script import Manager

from project import create_app, db
from project.models import Note
from project.utils import files_in_repo, get_file_contents

app = create_app()
manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    db.session.add(Note(title='Testing db', category='Git'))
    db.session.add(Note(title='Testing db2', category='Misc'))
    db.session.commit()


@manager.command
def init():
    filenames = files_in_repo()
    print(filenames)
    for file in filenames:
        print(get_file_contents(file))


@manager.command
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
