from flask import Flask, jsonify
import yfinance as yf
import time

app = Flask(__name__)

def get_cocoa_price_with_retry(max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            cacao = yf.Ticker("CC=F")
            data = cacao.history(period="1d")
            
            if data.empty:
                return {"error": "No data available for the specified ticker"}, 404
            
            last_close = data['Close'].iloc[-1]
            return {
                "ticker": "CC=F",
                "last_close_price": round(last_close, 2)
            }, 200
        
        except yfinance.exceptions.YFRateLimitError:
            # Wait for an exponentially increasing amount of time before retrying
            wait_time = 2 ** retries  # Exponential backoff: 2, 4, 8, 16, 32 seconds
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
        
        except Exception as e:
            return {"error": str(e)}, 500
    
    # If all retries fail, return an error message
    return {"error": "Failed to fetch data after multiple attempts due to rate limiting."}, 500

@app.route('/cocoa-price', methods=['GET'])
def get_cocoa_price():
    response, status_code = get_cocoa_price_with_retry()
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)