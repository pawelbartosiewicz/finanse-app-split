from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from datetime import datetime

from app.models import Transaction, User # Importujemy nasz model transakcji

# 1. Tworzymy Blueprint o nazwie 'main'
main_bp = Blueprint('main', __name__)




@main_bp.route('/test')
def testfunc():
    return jsonify({
        "message": "Hello test!"
    }),201

# --- STRONA GŁÓWNA ---
@main_bp.route('/')
def index():
    # Jeśli użytkownik jest już zalogowany, nie pokazujemy mu powitania,
    # tylko od razu kierujemy na dashboard.
    # if current_user.is_authenticated:
    if 1==1:
        # return redirect(url_for('main.dashboard'))
        return "You are logged in, hello!"
    
    # return render_template('index.html')
    return "You are not logged in, hello!"


# --- DASHBOARD (Tylko dla zalogowanych) ---
@main_bp.route('/dashboard')
def dashboardLogin():
    return jsonify({
        "message" : "Hello",
        "user" : current_user.id
    }),201



@main_bp.route('/api/showTransactions', methods=['GET'])
# @login_required
def showTransactions():
    if 1==1:
    # if current_user.is_authenticated:
        user = User.query.filter_by(id=1).first()
        tranasctions_json = []
        raw_transactions = user.transactions

        


        for t in raw_transactions:
            tranasctions_json.append({
                "id" : t.id,
                "category" : t.category,
                "op_type" : t.op_type,
                "amount" : t.amount,
                "currency" : t.currency,
                "date" : t.date,
                "description" : t.description,
                "createdAt" : t.createdAt
             })

        return jsonify({
            "data" : tranasctions_json
        })

    






# --- DODAWANIE TRANSAKCJI ---
@main_bp.route('/api/addTransaction', methods=['POST'])
# @login_required
def add_transaction():

    data = request.get_json()

    category=data.get('category')
    op_type=data.get('op_type')
    amount=float(data.get('amount'))
    currency=data.get('currency')
    date=datetime.now()
    description=data.get('description')
    createdAt=datetime.now()
       
    try:
        transactionToAdd = Transaction(
            user_id=current_user.id,
            category=category,
            op_type=op_type,
            amount=amount,
            currency=currency,
            date=date,
            description=description,
            createdAt=createdAt
        )

    # return jsonify({
    #     "userid" : transactionToAdd.user_id,
    #     "category" : transactionToAdd.category,
    #     "op_type" : transactionToAdd.op_type,
    #     "amount" : transactionToAdd.amount,
    #     "currency" : transactionToAdd.currency,
    #     "description" : transactionToAdd.description
    # })

        # Zapisujemy w bazie
        db.session.add(transactionToAdd)
        db.session.commit()
        
        return jsonify({
            "message": "Transaction added successfully!",
            "data" : transactionToAdd.__repr__()
        }),201
        
    except ValueError as e:
        return jsonify({
            "message": "Value error: " + str(e)
        }),400
    except Exception as e:
        db.session.rollback()
        return jsonify({

            "message": "Database error occurred, rolling back. Error: " + str(e)
        }),500

    # Wracamy na dashboard
    
    # return("Au ao")






