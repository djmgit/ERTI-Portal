import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app, db


#app.config.from_object(os.environ['APP_SETTINGS'])

if os.environ.get('DATABASE_URL') is None:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///versions.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/deep'
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = "THIS IS SECRET"

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

class Prebirth(db.Model):
    __tablename__ = 'Prebirth'

    id = db.Column('artcile_id', db.Integer, primary_key=True)
    month_no = db.Column(db.Integer)
    title = db.Column(db.String)
    article = db.Column(db.String)
    dos = db.Column(db.String)
    donts = db.Column(db.String)
    diet = db.Column(db.String)

    def __init__(self, month_no='', title='', article='', dos='', donts='', diet=''):
        self.month_no = month_no
        self.title = title
        self.article = article
        self.dos = dos
        self.donts = donts
        self.diet = diet



if __name__ == '__main__':
    manager.run()
