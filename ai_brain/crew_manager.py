import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from shared_models import MarketContext, TradeProposal

class AIBrain:
    def __init__(self):
        # 1. SETUP GROQ DIRECTLY
        # No "CrewAI" wrappers. No hidden OpenAI checks. Just pure Groq.
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile", 
            temperature=0.7
        )

    def start_debate(self, market_data: MarketContext) -> TradeProposal:
        """
        Runs the debate using a single powerful prompt instead of multiple agents.
        This is faster, cheaper, and crash-proof.
        """
        
        # 2. CONSTRUCT THE "MEGA-PROMPT"
        # We ask Llama-3 to simulate all three people at once.
        market_summary = market_data.summary()
        
        prompt = f"""
        You are an AI Investment Committee managing a crypto treasury.
        
        THE COMMITTEE MEMBERS:
        1. Warren (Boomer): Conservative, risk-averse, hates volatility.
        2. Chad (Degen): Risk-loving, chases hype and memes, uses slang.
        3. Atlas (Quant): Data-driven, cold, analytical, tie-breaker.

        MARKET DATA:
        {market_summary}

        TASK:
        Simulate a short debate between these three. Warren and Chad should argue. Atlas should decide.
        
        OUTPUT FORMAT:
        Return ONLY a JSON object (no markdown, no conversation text outside JSON) with this structure:
        {{
            "winner": "Name of the agent who won (Warren/Chad/Atlas)",
            "decision": "BUY", "SELL", or "HOLD",
            "amount_percent": 0.1,
            "reason": "A one-sentence summary of the winning logic",
            "asset": "{market_data.target_asset_symbol}"
        }}
        """

        # 3. INVOKE GROQ DIRECTLY
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            response_text = response.content
            return self._parse(response_text, market_data)
            
        except Exception as e:
            # Fallback if Groq API has a hiccup
            print(f"⚠️ Groq Raw Error: {e}")
            return TradeProposal("err", "System", "HOLD_Existing", market_data.target_asset_symbol, 0.0, "API Error")

    def _parse(self, text, context):
        try:
            # Clean up potential markdown wrappers
            clean_text = re.sub(r"```json", "", text).replace("```", "").strip()
            
            # Parse JSON
            data = json.loads(clean_text)
            
            return TradeProposal(
                proposal_id="fast-mode", 
                proposing_agent_name=data.get("winner", "Atlas"), 
                action=data.get("decision", "HOLD"), 
                target_asset_symbol=context.target_asset_symbol, 
                percentage_of_treasury_to_use=float(data.get("amount_percent", 0.0)), 
                reasoning_summary=data.get("reason", "Consensus reached")
            )
        except Exception as e:
            print(f"⚠️ Parse Error: {e} | Raw: {text}")
            return TradeProposal("err", "System", "HOLD_Existing", context.target_asset_symbol, 0.0, "Parse Error")
