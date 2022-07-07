from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import cloudinary
import stripe
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/system?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "!@#$%^&*()(*&^%$#@#$%^&*("
app.config["PAGE_SIZE"] = 6
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51JxWFsEMDYePyYSgY8abIK9kH8sQpy6XAOPsmuNDXzlqoH4QajY4ImmCi6VwzqULBqOdofL3DlgFYLk7915RTWR700ll6TxnDh'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51JxWFsEMDYePyYSgAtlinPmy9cxQ4LvFTKOy5jCOqeA8SYd0RoEIeETdRKsyancnv4mbfaOvyoQr5NCa5iySOJ1K004eufFLT5'
cloudinary.config(
    cloud_name="h-spkt-tphcm",
    api_key="141165373498883",
    api_secret="MJ_m50rggogFES5Mr2FFqWkptdQ"
)
db = SQLAlchemy(app=app)
admin = Admin(app=app, name="BUG AIRLINES", template_mode="bootstrap4")
my_login = LoginManager(app=app)

customer = {}
CART_KEY = "cart"
STAFF_CART_KEY = "staff-cart"