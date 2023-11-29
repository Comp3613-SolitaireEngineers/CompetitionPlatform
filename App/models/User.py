from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
import uuid

def generate_short_uuid():
    return str(uuid.uuid4())[:8]

class User(db.Model, UserMixin):
    __abstract__ = True
    __tablename__ = 'user'
    id = db.Column(db.String(120), primary_key=True, default=generate_short_uuid, server_default='gen_random_uuid()')
    uwi_id = db.Column(db.String(120), nullable=False, unique=True)
    username =  db.Column(db.String(120), nullable=False, unique=True)    
    email = db.Column(db.String(120), nullable=False, unique=True)    
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(120), nullable=False)

    def __init__(self, uwi_id, username, email, password):
        self.uwi_id = uwi_id
        self.username = username
        self.email = email
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'uwi_id': self.uwi_id,
            'username': self.username,
            'email': self.email
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)