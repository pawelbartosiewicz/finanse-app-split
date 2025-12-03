from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
import yfinance as yf
# import requests
# from datetime import datetime

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

