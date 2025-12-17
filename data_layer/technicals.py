import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    """
    Calculates indicators manually using Pandas to avoid complex dependencies like TA-Lib.
    """
    
    @staticmethod
    def calculate_rsi(df: pd.DataFrame, period: int = 14) -> float:
        """
        Relative Strength Index (RSI). 
        > 70 = Overbought (Sell signal for Quant)
        < 30 = Oversold (Buy signal for Quant)
        """
        if df.empty: return 50.0 # Neutral default
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Return the most recent RSI value
        return float(rsi.iloc[-1])

    @staticmethod
    def calculate_sma_200(df: pd.DataFrame) -> float:
        """
        200-period Simple Moving Average.
        The 'Boomer' agent loves this. If Price < SMA 200, it's a bear market.
        """
        if len(df) < 200: return 0.0
        return float(df['close'].rolling(window=200).mean().iloc[-1])

    @staticmethod
    def calculate_bollinger_width(df: pd.DataFrame, period: int = 20) -> float:
        """
        Bollinger Band Width.
        High width = High Volatility (Degen likes this).
        Low width = Squeeze/Consolidation.
        """
        if df.empty: return 0.0
        
        sma = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        
        width = (upper_band - lower_band) / sma
        return float(width.iloc[-1])
    