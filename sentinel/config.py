import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SOPS_DIR = DATA_DIR / "sops"
REGULATIONS_DIR = DATA_DIR / "regulations"

NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY", "")
NEBIUS_BASE_URL = "https://api.studio.nebius.com/v1/"
MODEL = "deepseek-ai/DeepSeek-V4-Pro"
MODEL_MAX_TOKENS = 16_000

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-opus-4-7"

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "sentinel-sops")

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

SNOWGLOBE_API_KEY = os.environ.get("SNOWGLOBE_API_KEY", "")

LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY", "")
if LANGSMITH_API_KEY:
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "sentinel-agent")
    os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"
EMBEDDING_DIMENSION = 4096

PRICING = {
    "deepseek-ai/DeepSeek-V4-Pro": {"input": 1.75, "output": 3.50},
    "claude-opus-4-7": {"input": 5.00, "output": 25.00},
}

SOP_BUSINESS_UNITS = [
    "01_ai_ml_engineering",
    "02_clinical_ai_products",
    "03_data_governance_privacy",
    "04_financial_services",
    "05_information_security",
    "06_it_operations",
    "07_human_resources",
    "08_legal_compliance",
    "09_product_engineering",
    "10_customer_operations",
]
