from flask import Blueprint, url_for, redirect, render_template, session, Response
import yfinance as yf
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64


route_bp = Blueprint("route", __name__)

stocks = {
    "reliance": {"name": "Reliance Industries", "symbol": "RELIANCE.NS"},
    "tcs": {"name": "TCS", "symbol": "TCS.NS"},
    "infosys": {"name": "Infosys", "symbol": "INFY.NS"},
    "hdfc": {"name": "HDFC Bank", "symbol": "HDFCBANK.NS"},
    "icici": {"name": "ICICI Bank", "symbol": "ICICIBANK.NS"},
    "itc": {"name": "ITC", "symbol": "ITC.NS"},
    "hul": {"name": "HUL", "symbol": "HINDUNILVR.NS"},
    "sbi": {"name": "SBI", "symbol": "SBIN.NS"},
    "airtel": {"name": "Airtel", "symbol": "BHARTIARTL.NS"},
    "lt": {"name": "L&T", "symbol": "LT.NS"},
}


def create_plot(plot_func):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    plot_func(ax)
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return base64.b64encode(img.getvalue()).decode()

@route_bp.route("/")
def home():
    names = []
    symbols = []
    market_cap = []
    prices = []

    for key in stocks:
        stock = stocks[key]
        names.append(stock["name"])
        symbols.append(stock["symbol"])

        tick = yf.Ticker(stock["symbol"])
        info = tick.info

        market_cap.append(info.get("marketCap", 0))
        prices.append(info.get("currentPrice", 0))
    most_valued = max(market_cap)
    index = market_cap.index(most_valued)
    

    top_stock = {
        "name" : names[index],
        "symbol" : symbols[index],
        "marketcap" : most_valued
    }

    mc_pie = create_plot(
        lambda ax:( 
            ax.pie(market_cap, labels = names,autopct='%1.1f%%'),
            ax.set_title("Market Cap PIE")
        )
    )
    mc_bar = create_plot(
        lambda ax:( 
            ax.bar(names, market_cap),
            ax.set_title("Market Cap BAR"),
            ax.set_xticklabels(names, rotation=45, ha='right')
        )
    )


    return render_template("index.html", mc_pie = mc_pie,mc_bar=mc_bar, top_stock = top_stock, names=names, symbols =symbols)



@route_bp.route("/stock/<key>")
def stock_page(key):
    stock = stocks.get(key) 
    symbol = stock["symbol"]
    tick = yf.Ticker(symbol)
    hist = tick.history(period ="1y")
    data = hist.reset_index()[["Date", "Close"]]

    prices = data["Close"].tolist()
    dates = data["Date"].tolist()

    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

    data["Close"] = data["Close"].round(2)
    result = data.values.tolist()
    
    length = len(result)
    mc_graph = create_plot(
        lambda ax: (
            ax.plot(dates, prices),
            ax.set_title("Growth Graph"),
            ax.grid(True)
        )
    )
    if not stock:
        return "Stock not found"
    return render_template("analytics.html", result = result, length = length, symbol = symbol, mc_graph=mc_graph)