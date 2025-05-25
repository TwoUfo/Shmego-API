from api import db


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String(20), primary_key=True, nullable=False)
    role = db.Column(
        db.Enum("admin", "op", name="role_enum"),
        nullable=False,
        default="op",
    )
