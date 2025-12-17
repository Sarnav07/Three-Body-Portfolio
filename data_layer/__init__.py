import requests
import random
from datetime import datetime
from shared_models import MarketContext

def get_fear_and_greed_index() -> tuple[int, str]:
    print(f"    👀 [SocialScanner] Fetching Crypto Fear & Greed Index...")
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        data = response.json()
        score = int(data['data'][0]['value'])
        classification = data['data'][0]['value_classification']
        
        sentiment_str = "NEUTRAL"
        if score > 60: sentiment_str = "BULLISH"
        elif score < 40: sentiment_str = "BEARISH"
            
        print(f"    ✅ [SocialScanner] Index: {score}/100 ({classification}). Sentiment: {sentiment_str}")
        return score, sentiment_str
    except Exception as e:
        print(f"    ❌ [SocialScanner] Error: {e}")
        return 50, "NEUTRAL"

def fetch_market_context(ticker: str) -> MarketContext:
    print(f"--- Fetching Market Data for {ticker} ---")
    
    # Standard Mock Price (Simulation)
    base_price = 85000.0 if "BTC" in ticker else 3000.0
    volatility = random.uniform(-0.02, 0.02)
    current_price = base_price * (1 + volatility)
    
    # Standard Random RSI
    rsi = random.uniform(30, 70)
    
    # Real Sentiment
    fng_score, sentiment = get_fear_and_greed_index()

    return MarketContext(
        timestamp=datetime.now(),
        target_asset_symbol=ticker,
        target_asset_address="0xMockWrapper",
        quote_asset_symbol="USDT",
        current_price=current_price,
        rsi_14=rsi,
        sma_200=base_price * 0.95,
        social_mention_count_24h=fng_score * 10,
        dominant_sentiment=sentiment
    )