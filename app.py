from flask import Flask, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currency_converter.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_currency = db.Column(db.String(3))
    target_currency = db.Column(db.String(3))
    base_amount = db.Column(db.Float)
    target_amount = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/convert', methods=['POST'])
def convert_currency():
    # Get the request data
    data = request.get_json()
    base_currency = data['base_currency']
    target_currency = data['target_currency']
    base_amount = float(data['base_amount'])

    # Make the API request
    api_key = '21db46ddb5524d9a80a2de88867b86ff'
    api_url = f'https://openexchangerates.org/api/latest.json?app_id={api_key}'
    response = requests.get(api_url)
    rates = response.json()['rates']

    # Calculate the target amount
    target_rate = rates[target_currency]
    base_rate = rates[base_currency]
    target_amount = round((base_amount / base_rate) * target_rate, 2)

    # Save the transaction to the database
    transaction = Transaction(base_currency=base_currency, target_currency=target_currency, 
                              base_amount=base_amount, target_amount=target_amount)
    db.session.add(transaction)
    db.session.commit()

    # Return the result
    return jsonify({'target_amount': target_amount})

if __name__ == '__main__':
    app.run(debug=True)