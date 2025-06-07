from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Input parameters
    beam_type = db.Column(db.String(20), nullable=False)
    length_mm = db.Column(db.Float, nullable=False)
    width_mm = db.Column(db.Float, nullable=False)
    depth_mm = db.Column(db.Float, nullable=False)
    reinforcement_percent = db.Column(db.Float, nullable=False)
    load_kn = db.Column(db.Float, nullable=False)
    
    # Prediction result
    predicted_deflection_mm = db.Column(db.Float, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert prediction to dictionary for export"""
        return {
            'id': self.id,
            'beam_type': self.beam_type,
            'length_mm': self.length_mm,
            'width_mm': self.width_mm,
            'depth_mm': self.depth_mm,
            'reinforcement_percent': self.reinforcement_percent,
            'load_kn': self.load_kn,
            'predicted_deflection_mm': self.predicted_deflection_mm,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f'<Prediction {self.id} for User {self.user_id}>'
