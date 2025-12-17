# shared_models.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime

# ==========================================
# INPUT DATA (Senses -> Brain)
# ==========================================
@dataclass
class MarketContext:
    """
    A snapshot of market conditions passed to the AI Agents.
    The 'data_layer' produces this. The 'ai_brain' consumes it.
    """
    timestamp: datetime
    target_asset_symbol: str  # e.g., "ETH", "PEPE"
    target_asset_address: Optional[str] # On-chain address if known
    quote_asset_symbol: str   # e.g., "USDC"
    
    # Raw Price Data
    current_price: float
    
    # Technical Indicators
    rsi_14: Optional[float] = None
    sma_200: Optional[float] = None
    bollinger_band_width: Optional[float] = None
    
    # Sentiment Data
    social_mention_count_24h: Optional[int] = None
    dominant_sentiment: Literal["BULLISH", "BEARISH", "NEUTRAL"] = "NEUTRAL"

    def summary(self) -> str:
        """Helper to convert the data into a readable string for the LLM prompt."""
        return (
            f"Market Context for {self.target_asset_symbol}/{self.quote_asset_symbol} at {self.timestamp}:\n"
            f"- Price: ${self.current_price:.4f}\n"
            f"- RSI(14): {self.rsi_14 if self.rsi_14 else 'N/A'}\n"
            f"- Social Mentions (24h): {self.social_mention_count_24h if self.social_mention_count_24h else 'N/A'}\n"
            f"- Sentiment: {self.dominant_sentiment}"
        )


# ==========================================
# OUTPUT DATA (Brain -> Orchestrator)
# ==========================================
@dataclass
class TradeProposal:
    """
    The structured output from the AI debate.
    The 'ai_brain' produces this.
    """
    proposal_id: str            # Unique UUID for tracking
    proposing_agent_name: str   # Who started this? e.g., "Agent B (Degen)"
    
    # The actual trade details
    action: Literal["BUY", "SELL", "HOLD_Existing"]
    target_asset_symbol: str    # e.g., "PEPE"
    
    # How much of our stablecoin treasury to use (e.g., 0.1 for 10%)
    # Using percentages is safer for bots than raw numbers.
    percentage_of_treasury_to_use: float 
    
    reasoning_summary: str      # A 1-sentence summary of why they want this.


# ==========================================
# EXECUTION TRIGGER (Orchestrator -> Blockchain)
# ==========================================
@dataclass
class VoteResult:
    """
    The final tally used to trigger blockchain execution.
    The 'orchestrator' creates this. The 'execution_layer' consumes it.
    """
    proposal: TradeProposal
    passed: bool                        # Did it get >= 2/3?
    total_votes_yea: int
    total_votes_nay: int
    
    # Which agents voted YEA (needed to know which keys to use for signing)
    yea_voter_names: List[str] = field(default_factory=list)
    
    # Added during the execution phase: The cryptographic signatures of the Yea voters
    # Key = Agent Name, Value = Hex Signature String
    signatures: Dict[str, str] = field(default_factory=dict)