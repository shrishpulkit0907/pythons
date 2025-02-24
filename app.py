import yfinance as yf 
cacao = yf.Ticker("CC=F")
data = cacao.history(period="1d") 
last_close = data['Close'].iloc[-1] 
print(last_close)