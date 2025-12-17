import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class DiscordNotifier:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        
        if not self.webhook_url:
            print("⚠️  Warning: DISCORD_WEBHOOK_URL not found in .env. Notifications disabled.")

    def post_trade_decision(self, ticker: str, decision: str, agent: str, reason: str, passed: bool):
        """
        Formats a beautiful Embed message and sends it to Discord.
        """
        if not self.webhook_url:
            return

        # Choose a color based on the decision
        color = 0x808080 # Grey (Hold)
        if decision == "BUY":
            color = 0x00ff00 # Green
        elif decision == "SELL":
            color = 0xff0000 # Red

        # Status Emoji
        status_emoji = "✅ Executed" if passed else "❌ Rejected"
        if decision == "HOLD_Existing":
            status_emoji = "zzZ Sleeping"

        # Construct the Embed Data (Rich Text)
        data = {
            "username": "The Three-Body Portfolio",
            "avatar_url": "https://i.imgur.com/8Q8qg9L.png", # Optional cool icon
            "embeds": [
                {
                    "title": f"{status_emoji}: {decision} {ticker}",
                    "description": f"**Winner:** {agent}\n**Logic:** {reason}",
                    "color": color,
                    "footer": {
                        "text": "Three-Body DAO • V1 Prototype"
                    }
                }
            ]
        }

        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 204:
                print("   💬 Discord Notification Sent!")
            else:
                print(f"   ❌ Discord Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Discord Connection Failed: {e}")

# Simple Test Block
if __name__ == "__main__":
    bot = DiscordNotifier()
    bot.post_trade_decision("BTC/USDT", "BUY", "Chad (The Degen)", "RSI is super low!", True)