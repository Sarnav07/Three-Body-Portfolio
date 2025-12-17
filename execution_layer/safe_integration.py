import os
import json
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
from shared_models import TradeProposal

class SafeExecutor:
    def __init__(self):
        load_dotenv()
        self.rpc_url = os.getenv("WEB3_RPC_URL", "http://127.0.0.1:8545")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contract_address = os.getenv("SAFE_ADDRESS")
        
        # Load the Signer (We only need one for the Counter test)
        self.private_key = os.getenv("PRIVATE_KEY_AGENT_B_DEGEN")
        self.account = Account.from_key(self.private_key)

        # 1. Define the ABI (Interface) for the Counter Contract
        # In a real app, we load this from a file. For now, we hardcode the "increment" function.
        self.abi = '[{"type":"function","name":"increment","inputs":[],"outputs":[],"stateMutability":"nonpayable"}]'
        
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

    def execute_vote(self, proposal: TradeProposal, voters: list):
        print(f"\n⚡ EXECUTING ON BLOCKCHAIN: {proposal.action} {proposal.target_asset_symbol}")
        
        if not self.contract_address:
            print("❌ Error: SAFE_ADDRESS not found in .env")
            return False

        try:
            # 2. Build the Transaction
            # We are telling the blockchain: "Run the increment() function"
            tx = self.contract.functions.increment().build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # 3. Sign it (The "Hands" moving)
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            
            # 4. Broadcast it (The "Go" Button)
            print(f"    🚀 Broadcasting transaction to Anvil...")
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            # 5. Wait for Receipt
            print(f"    ⏳ Waiting for confirmation...")
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"    ✅ TRANSACTION CONFIRMED!")
            print(f"    🔗 Hash: {self.w3.to_hex(tx_hash)}")
            print(f"    ⛽ Gas Used: {receipt['gasUsed']}")
            return True

        except Exception as e:
            print(f"    ❌ Blockchain Error: {e}")
            return False