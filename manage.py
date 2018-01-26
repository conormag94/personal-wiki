from flask_script import Manager

from project import create_app
from project.utils import files_in_repo, get_file_contents

app = create_app()
manager = Manager(app)

@manager.command
def init():
    filenames = files_in_repo()
    print(filenames)
    for file in filenames:
        print(get_file_contents(file))

if __name__ == '__main__':
    manager.run()
