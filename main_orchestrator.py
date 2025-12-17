import sys
import time
import os
import json
from datetime import datetime

# Disable Rich Tracebacks to prevent the recursion crash
os.environ["RICH_TRACEBACK"] = "0"

# Imports
try:
    from data_layer import fetch_market_context
    from execution_layer.safe_integration import SafeExecutor
    from frontend_layer.discord_bot import DiscordNotifier
    from ai_brain.crew_manager import AIBrain
    from shared_models import TradeProposal, MarketContext
    AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Import Error: {e}")
    AI_AVAILABLE = False

# --- CONFIGURATION ---
SLEEP_DELAY_SECONDS = 300  # 5 Minutes between cycles
TICKER = "BTC/USDT"

class Orchestrator:
    def __init__(self):
        self.executor = SafeExecutor()
        self.notifier = DiscordNotifier()
        self.brain = None
        if AI_AVAILABLE:
            try:
                self.brain = AIBrain()
                print("✅ AI Brain Connected (Groq)")
            except Exception as e:
                print(f"⚠️ AI Init Failed: {e}")

    def mock_brain_decision(self, context):
        print("\n[🤖 MOCK BRAIN] Fallback active...")
        if context.rsi_14 and context.rsi_14 < 30:
            return TradeProposal("mock", "Chad", "BUY", context.target_asset_symbol, 0.1, "RSI Oversold")
        return TradeProposal("mock", "Warren", "HOLD_Existing", context.target_asset_symbol, 0.0, "Safety first")

    def run_cycle(self, ticker="BTC/USDT"):
        print(f"\n{'='*40}")
        print(f"🚀 STARTING CYCLE: {ticker} at {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*40}")
        
        try:
            # 1. SENSE
            print("--- SENSING ---")
            market_context = fetch_market_context(ticker)
            print(f"Price: {market_context.current_price:.2f} | RSI: {market_context.rsi_14:.2f}")

            # 2. THINK
            print("--- THINKING ---")
            proposal = None
            
            if self.brain:
                try:
                    proposal = self.brain.start_debate(market_context)
                except Exception as e:
                    print(f"❌ Brain Error: {e}")
                    proposal = self.mock_brain_decision(market_context)
            else:
                proposal = self.mock_brain_decision(market_context)

            print(f"👉 DECISION: {proposal.action} by {proposal.proposing_agent_name}")
            print(f"👉 REASON: {proposal.reasoning_summary}")

            # 3. ACT
            print("--- EXECUTING ---")
            tx_hash = "N/A"
            if proposal.action != "HOLD_Existing":
                success = self.executor.execute_vote(proposal, ["Chad", "Atlas"])
                if success:
                    print("✅ Transaction Signed & Broadcasted")
                    # In a real app, we would capture the hash from the executor
                    tx_hash = "0x..." 
                else:
                    print("❌ Transaction Failed")
            else:
                print("🛑 No Action Taken (HOLD)")
            
            # 4. NOTIFY
            print("--- NOTIFYING ---")
            self.notifier.post_trade_decision(
                ticker, 
                proposal.action, 
                proposal.proposing_agent_name, 
                proposal.reasoning_summary, 
                True
            )
            print("💬 Discord Sent")

            # --- 5. SAVE STATE FOR DASHBOARD (NEW!) ---
            dashboard_data = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "ticker": ticker,
                "price": market_context.current_price,
                "rsi": market_context.rsi_14,
                "sentiment": market_context.dominant_sentiment,
                "decision": proposal.action,
                "agent": proposal.proposing_agent_name,
                "reason": proposal.reasoning_summary,
                "tx_hash": tx_hash
            }
            
            # Save to a JSON file that the website can read
            with open("frontend_layer/dashboard_state.json", "w") as f:
                json.dump(dashboard_data, f)
            print("💾 Dashboard State Updated")
            # -----------------------------------------------
            
        except Exception as e:
            print(f"❌ CYCLE ERROR: {e}")

    def start_autonomous_mode(self):
        print(f"\n🤖 SYSTEM ONLINE: Autonomous Mode Activated")
        print(f"⏱️  Interval: {SLEEP_DELAY_SECONDS} seconds")
        print("---------------------------------------------------")
        
        while True:
            try:
                self.run_cycle(TICKER)
                
                print(f"\n💤 Cycle Complete. Sleeping for {SLEEP_DELAY_SECONDS} seconds...")
                print("---------------------------------------------------")
                time.sleep(SLEEP_DELAY_SECONDS)
                
            except KeyboardInterrupt:
                print("\n🛑 MANUAL OVERRIDE: Stopping Bot.")
                sys.exit(0)
            except Exception as e:
                print(f"❌ CRITICAL ERROR: {e}")
                print("⚠️  Retrying in 60 seconds...")
                time.sleep(60)

if __name__ == "__main__":
    bot = Orchestrator()
    bot.start_autonomous_mode()