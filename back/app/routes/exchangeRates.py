from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
import yfinance as yf
import requests
# from datetime import datetime

# from app.models import Transaction, User # Importujemy nasz model transakcji








exchanges_bp = Blueprint('exchanges', __name__)


@exchanges_bp.route('/api/exchangeRates/<symbol>', methods=['GET'])
def getExchangeRates(symbol):
    # przyklad - kurs USD -- https://api.nbp.pl/api/exchangerates/rates/a/usd
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{symbol}?format=json"
    try:
        result = requests.get(url, timeout=10)
        result.raise_for_status()
        
        data = result.json()




        return jsonify({
            "exchangeRateDate" : data['rates'][0]['effectiveDate'],
            "exchangeRateValue" : data['rates'][0]['mid'],
            "code" : data['code'],
            # "fullData" : data
        }),200


    except requests.exceptions.HTTPError:
        # Ten błąd wyłapie sytuację, gdy waluta nie istnieje (kod 404 z NBP)
        return jsonify({
            "error": f"Waluta '{symbol}' nie została znaleziona w tabeli A NBP."
        }), 404


    except Exception as e:
        return jsonify({
            "message" : "Error while fetching data from NBP",
            "error" : str(e)
        }),500
    
@exchanges_bp.route('/api/exchangeRates1', methods=['GET']) ## pobranie kursu przez backend
def testtest():
    return getExchangeRates(symbol="CHF")