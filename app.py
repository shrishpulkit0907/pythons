from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/cocoa-price', methods=['GET'])
def get_cocoa_price():
    try:
        # Fetch Cocoa futures data
        cacao = yf.Ticker("CC=F")
        data = cacao.history(period="1d")
        
        # Check if data is empty
        if data.empty:
            return jsonify({"error": "No data available for the specified ticker"}), 404
        
        # Extract the last closing price
        last_close = data['Close'].iloc[-1]
        
        # Return the result as JSON
        return jsonify({
            "ticker": "CC=F",
            "last_close_price": round(last_close, 2)
        }), 200
    
    except Exception as e:
        # Handle any exceptions and return an error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)