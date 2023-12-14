from flaskshop.account.models import User as BaseUser
from flaskshop.product.models import Product as BaseProduct
from flaskshop.database import Column, Model, db


class Subdomain(Model):
    __tablename__ = "shop_subdomain"
    name = Column(db.String(255), unique=True)


class User(BaseUser):
    __tablename__ = "account_user"
    domain_id = Column(db.Integer())

    @property
    def domain(self):
        return self.subdomain

class Product(BaseProduct):
    __tablename__ = "product_product"
    domain_id = Column(db.Integer())

    @property
    def domain(self):
        return self.subdomain

def find_subdomain(subdomain_name):
    return Subdomain.query.filter_by(name=subdomain_name).first()
