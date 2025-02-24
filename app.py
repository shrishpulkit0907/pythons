from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/get_cacao_price', methods=['GET'])
def get_cacao_price():
    try:
        cacao = yf.Ticker("CC=F")
        data = cacao.history(period="1d")
        last_close = data['Close'].iloc[-1]
        return jsonify({"last_close_price": last_close})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
