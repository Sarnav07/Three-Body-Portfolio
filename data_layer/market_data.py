import ccxt
import pandas as pd
from typing import Tuple, Optional

class MarketDataProvider:
    def __init__(self, exchange_id: str = 'binance'):
        # We use a public instance (no API keys needed just for fetching prices)
        try:
            self.exchange = getattr(ccxt, exchange_id)()
        except AttributeError:
            print(f"Warning: Exchange {exchange_id} not found, defaulting to Binance.")
            self.exchange = ccxt.binance()

    def fetch_current_price(self, symbol: str) -> float:
        """
        Fetches the latest ticker price.
        Symbol format example: 'BTC/USDT' or 'PEPE/USDT'
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return float(ticker['last'])
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return 0.0

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 200) -> pd.DataFrame:
        """
        Fetches historical candle data for technical analysis.
        Returns a Pandas DataFrame with columns: [timestamp, open, high, low, close, volume]
        """
        try:
            # fetch_ohlcv returns a list of lists
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching candles for {symbol}: {e}")
            return pd.DataFrame()