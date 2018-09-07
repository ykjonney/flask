from validators.database import db as orm
from flask_mail import Mail
from flask_uploads import configure_uploads,uploaded_file,IMAGES


def ext(app):
    db=orm
    mail=Mail(app=app)
    product_img_upload=uploaded_file('product_img',IMAGES)
    configure_uploads(app,(product_img_upload,))
    db.init_app(app)