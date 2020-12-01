"""
Populate Database with latest stock prices.

Note:
This script is meant to be schedule through the OS
"""

import sqlite3
import config
import tulipy
import numpy as np
import alpaca_trade_api as tradeapi
import datetime as dt

# Connect to Database and Fetch Stock names and IDS
connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("""
    SELECT id, symbol, name FROM stocks_stock
""")
rows = cursor.fetchall()
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

# Connect to Alpaca and Fetch Price Data.
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.ALPACA_PAPER_URL)
chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i: i+chunk_size]
    barsets = api.get_barset(symbol_chunk, 'day')

    # Loop over the Keys in the barsets dictionary
    for symbol in barsets:
        print(f"Processing symbol {symbol}")

        recent_closes = [bar.c for bar in barsets[symbol]]
        # Loop through each bar for the current symbol in the dictionary
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            
            if len(recent_closes) >= 50 and dt.date.today().isoformat() == bar.t.date().isoformat():
                sma_20 = tulipy.sma(np.array(recent_closes), period=20)[-1]
                sma_50 = tulipy.sma(np.array(recent_closes), period=50)[-1]
                rsi_14 = tulipy.rsi(np.array(recent_closes), period=14)[-1]

            else:
                sma_20, sma_50, rsi_14 = None, None, None
            
            cursor.execute("""
                INSERT INTO stocks_stockprice (stock_id_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_20, sma_50, rsi_14))

connection.commit()