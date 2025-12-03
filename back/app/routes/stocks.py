from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
import yfinance as yf
from app.models import Portfolio, Transaction
# import requests
from datetime import datetime

# from app.models import Transaction, User # Importujemy nasz model transakcji








stocks_bp = Blueprint('stocks', __name__)


# --- STRONA GŁÓWNA ---
@stocks_bp.route('/api/stocks/<ticker>', methods=['GET'])
def getStockData(ticker): 
    try:
        dat = yf.Ticker(ticker)
        # dat.info
        # dat.calendar
        # dat.analyst_price_targets
        # dat.quarterly_income_stmt
        # dat.history(period='1mo')
        # dat.option_chain(dat.options[0]).calls
    

        return jsonify({
            "message" : "Data fetched for "+ticker,
            "stocks_info" : {
                "info": dat.info,
                "calendar": dat.calendar,
                "analyst_price_targets": dat.analyst_price_targets,
                # "quarterly_income_stmt": dat.quarterly_income_stmt.to_json()
                # "history" : dat.history(period='1mo').to_json()
                # "history": dat.history(period='1mo').reset_index().to_dict(),
                # "option_chain_calls": dat.option_chain(dat.options[0]).calls.reset_index().to_dict()
            }

        }),200
    
    except Exception as e:
        return jsonify({
            "error" : str(e)
        }), 500




@stocks_bp.route('/api/addStocks', methods=['POST'])
# @login_required
def buyStocks():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data found"
        }),400
    
    ticker = data.get('ticker')
    quantity = data.get('quantity')
    buy_price = data.get('buy_price')
    user_id = 1
    currency = data.get('currency')

    if not ticker or not quantity or not buy_price or not currency:
        return jsonify({
            "error": "Missing required fields"
        }),400

    currentStock = Portfolio.query.filter_by(user_id=user_id, ticker=ticker).first()

    


    
    if currentStock: #jeżeli rekord już istnieje



        try:



            oldStockValue = (currentStock.quantity * currentStock.avg_buy_price)
            newStockValue = (quantity * buy_price)

            totalCost = oldStockValue + newStockValue
            totalQuantity = quantity + currentStock.quantity

            currentStock.avg_buy_price = totalCost / totalQuantity
            currentStock.quantity = totalQuantity

            currentStock.updatedAt = datetime.utcnow()

            transactionHistoryRecord = Transaction(
                user_id=1,
                ticker=ticker,
                category="Stocks",
                op_type="buy",
                amount=buy_price,
                currency=currency,
                date=datetime.utcnow(),
                createdAt=datetime.utcnow()
            )

            db.session.add(transactionHistoryRecord)

            db.session.commit()
            return jsonify({
                "message": "Stock purchase updated successfully!"
            }),200

        except Exception as e:
            return jsonify({
                "error": f"Error: {str(e)}"
            }),500

    else: # jezeli rekordu jeszcze nie ma -> dodaj

        try:
            # quantity = float(quantity)
            # buy_price = float(buy_price)

            # if quantity <= 0:
            #     return jsonify({
            #         "error": "Quantity must be greater than zero"
            #     }),400

            # if buy_price <= 0:
            #     return jsonify({
            #         "error" : "Price must be greater than zero"
            #     }),400
            
            # ticker = str(ticker).upper().strip()
            # if len(currency != 3):
            #     return jsonify({
            #         "error": "Currency code must be 3 exactly characters long"
            #     }),400
            
            transactionHistoryRecord = Transaction(
                user_id=1,
                ticker=ticker,
                category="Stocks",
                op_type="buy",
                amount=buy_price,
                currency=currency,
                date=datetime.utcnow(),
                createdAt=datetime.utcnow()
            )

            stockToRegister = Portfolio(
                user_id=user_id,
                ticker=ticker,
                quantity=quantity,
                avg_buy_price=buy_price,
                currency=currency
            )

            db.session.add(transactionHistoryRecord)
            db.session.add(stockToRegister)
            db.session.commit()
            return jsonify({
                "message": "Stock added to portfolio successfully!",
                "data" : stockToRegister.__repr__()
            }), 201

        except Exception as e:
            return jsonify({
                "error": str(e)
            })


