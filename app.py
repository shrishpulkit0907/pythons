from flask import Flask, jsonify
import yfinance as yf
import time

app = Flask(__name__)

# Simple caching mechanism
cache = {}
CACHE_DURATION = 60  # seconds

@app.route('/cacao/price', methods=['GET'])
def get_cacao_price():
    current_time = time.time()
    
    if 'price' in cache:
        cached_time, cached_price = cache['price']
        if current_time - cached_time < CACHE_DURATION:
            return jsonify(price=cached_price)

    cacao = yf.Ticker("CC=F")
    data = cacao.history(period="1d")
    last_close = data['Close'].iloc[-1]
    
    # Update cache
    cache['price'] = (current_time, last_close)
    return jsonify(price=last_close)

if __name__ == "__main__":
    app.run()