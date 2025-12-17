import random
import os
from typing import Tuple

class SocialScanner:
    def __init__(self):
        # We check if keys exist. If not, we use mock mode.
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.use_mock = not self.reddit_client_id

    def get_sentiment(self, symbol: str) -> Tuple[int, str]:
        """
        Returns (Mention Count, Sentiment String)
        """
        if self.use_mock:
            return self._mock_sentiment(symbol)
        
        # TODO: Implement real PRAW Reddit scraping here later
        # For now, fallback to mock to prevent crashes
        return self._mock_sentiment(symbol)

    def _mock_sentiment(self, symbol: str) -> Tuple[int, str]:
        """
        Simulates social media noise for testing.
        """
        print(f"[SocialScanner] mocking data for {symbol} (No API keys found)")
        
        # Randomly generate "hype"
        mentions = random.randint(50, 5000)
        
        sentiment_score = random.random() # 0.0 to 1.0
        
        if sentiment_score > 0.6:
            sentiment = "BULLISH"
        elif sentiment_score < 0.4:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"
            
        return mentions, sentiment