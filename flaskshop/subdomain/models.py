from flaskshop.database import Column, Model, db


class Subdomain(Model):
    __tablename__ = "shop_subdomain"
    name = Column(db.String(255), unique=True)

def find_subdomain(subdomain_name):
    return Subdomain.query.filter_by(name=subdomain_name).first()
