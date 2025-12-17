import os
from dotenv import load_dotenv
from eth_account import Account
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class KeyVault:
    """
    Securely manages access to the Agents' private keys.
    """
    
    def __init__(self):
        # We map the internal Agent Names to the Environment Variable keys
        self.agent_map = {
            "Warren (The Boomer)": "PRIVATE_KEY_AGENT_A_BOOMER",
            "Chad (The Degen)": "PRIVATE_KEY_AGENT_B_DEGEN",
            "Atlas (The Quant)": "PRIVATE_KEY_AGENT_C_QUANT"
        }

    def get_agent_account(self, agent_name: str) -> Optional[Account]:
        """
        Retrieves the web3.py Account object for a specific agent.
        """
        env_var_name = self.agent_map.get(agent_name)
        
        if not env_var_name:
            print(f"❌ Error: No key mapping found for agent '{agent_name}'")
            return None
            
        private_key = os.getenv(env_var_name)
        
        if not private_key:
            print(f"❌ Error: Environment variable {env_var_name} is empty!")
            return None
            
        try:
            # Create the local account object (does not connect to network yet)
            return Account.from_key(private_key)
        except Exception as e:
            print(f"❌ Error loading key for {agent_name}: {e}")
            return None

    def get_public_address(self, agent_name: str) -> str:
        """Helper to just get the public address (safe to share)"""
        account = self.get_agent_account(agent_name)
        if account:
            return account.address
        return "Unknown"