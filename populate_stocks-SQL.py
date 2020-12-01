"""
Populate Database with stock universe.
"""

import sqlite3
import config
import alpaca_trade_api as tradeapi

# Make sure to use a path the scheduler can get to
connection = sqlite3.connect(config.DB_FILE)

# This turns the rows returned after a query into a dictionary in which you can access values by key.
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stocks_stock
""")
rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]


api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.ALPACA_PAPER_URL)
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("""
                INSERT INTO stocks_stock (symbol, name, exchange, shortable) VALUES (?, ?, ?, ?)
            """, (asset.symbol, asset.name, asset.exchange, asset.shortable))
    except Exception as e:
        print(asset.symbol)
        print(e)
    
connection.commit()