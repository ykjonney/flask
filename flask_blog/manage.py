from flask_migrate import Migrate,MigrateCommand

from models.user import User
from flask_script import Manager
from app import app

from validators.database import db

manager=Manager(app=app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)
@manager.command
def list_ruote():
    for route in app.url_map.iter_rules():
        print(route)

@manager.option('-n','--number',dest='number',default=10)
def load_user(number):
    for i in range(int(number)):
        user=User(
            username='demo'+str(i),
            password='123456',
            email='demo'+str(i)+'@eamaple,com',
            is_active=1,
            is_verify=1,
        )
        try :
            user.save()
        except BaseException:
            print('demo'+str(i),'load_error')
            continue
        print('load over')
@manager.command
def reset_db():
    db.drop_all()
    db.create_all()

if __name__=='__main__':
   manager.run()



