# 🤖 Three-Body Portfolio: Autonomous AI Hedge Fund Agent

**A fully autonomous trading agent that combines Sentiment Analysis, Large Language Models (LLMs), and Blockchain Execution.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Solidity](https://img.shields.io/badge/Solidity-0.8.19-black)
![Sepolia](https://img.shields.io/badge/Network-Sepolia%20Testnet-green)
![Groq](https://img.shields.io/badge/AI-Llama3%20via%20Groq-orange)

## 🚀 Overview
This project implements a "Three-Body" architecture to solve automated decision-making in volatile markets. Instead of relying on a single algorithm, it uses a consensus mechanism between three distinct layers:

1.  **The Eyes (Sensing):** Real-time fetching of market data (Price, RSI) and social sentiment (Fear & Greed Index).
2.  **The Brain (Thinking):** A Groq-powered AI Agent (Llama 3) that debates strategy ("Chad" vs "Warren" personas) to form a trade proposal.
3.  **The Hands (Acting):** A secure execution layer that signs and broadcasts transactions directly to the Ethereum Sepolia Testnet.

## 🛠️ Architecture
- **Orchestrator:** `main_orchestrator.py` - The central nervous system that runs the infinite loop.
- **AI Brain:** `ai_brain/` - Uses Prompt Engineering to simulate a hedge fund committee.
- **Frontend:** `frontend_layer/` - A Streamlit dashboard for real-time monitoring of the bot's "thoughts" and actions.
- **Smart Contracts:** `contracts/` - Solidity contracts (Foundry) for on-chain interaction.

## ⚡ Quick Start
### Prerequisites
- Python 3.10+
- Foundry (for smart contracts)
- Groq API Key
- Ethereum Sepolia Wallet

### Installation
```bash
# Clone the repo
git clone [https://github.com/Sarnav07/Three-Body-Portfolio.git](https://github.com/Sarnav07/Three-Body-Portfolio.git)
cd Three-Body-Portfolio

# Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# (Add your PRIVATE_KEY and API_KEY in .env)
Run the Agent
Bash

python main_orchestrator.py
📊 Dashboard
To see the agent's brain in real-time:

Bash

streamlit run frontend_layer/app.py
🛡️ Security
Private Keys are never hardcoded and are loaded via dotenv.

GitIgnore is configured to exclude sensitive environment files.

📜 License
MIT License