from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Model Użytkownika
# Dziedziczymy po UserMixin, żeby Flask-Login "rozumiał" tego użytkownika
class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Nazwa tabeli w bazie

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacja: Jeden użytkownik ma wiele transakcji
    # 'backref' tworzy w transakcji pole 'owner', żebyś mógł pisać transaction.owner
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

    # Metoda do ustawiania hasła (tworzy hasz)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Metoda do sprawdzania hasła
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# 2. Model Transakcji
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    # Klucz obcy - łączy transakcję z id użytkownika
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    category = db.Column(db.String(50), nullable=False)
    op_type = db.Column(db.String(20), nullable=False)  
    amount = db.Column(db.Float, nullable=False)        
    currency = db.Column(db.String(3), default='PLN')   
    date = db.Column(db.DateTime, nullable=False) 
    description = db.Column(db.String(200))             
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id} - User {self.user_id} - Category { self.category } - Operation Type {self.op_type} - Amount {self.amount} - Currency {self.currency}>'