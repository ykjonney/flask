from flask_mail import Mail
from flask_migrate import Migrate
from flask_uploads import configure_uploads,uploaded_file,IMAGES

from App.database import db
# product_img_upload=uploaded_file('product_img',IMAGES)
mail = Mail()
migrate=Migrate(db)
def ext(app):

    mail.init_app(app)
    migrate.init_app(app=app)
    # App.config['UPLOAD_FOLDER'] = '/uploads'
    # App.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg', 'pdf']
    # # limit kyc upload 10MB
    # App.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    # configure_uploads(app,product_img_upload)
    db.init_app(app)