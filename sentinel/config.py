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
NEBIUS_MODELS = {
    "v3": "dedicated/deepseek-ai/DeepSeek-V3-0324-V7H70dy0RIqd",
    "v4": "deepseek-ai/DeepSeek-V4-Pro",
}
MODEL = NEBIUS_MODELS.get(os.environ.get("NEBIUS_MODEL", "v4"), NEBIUS_MODELS["v4"])
MODEL_MAX_TOKENS = 16_000
REASONING_EFFORT = os.environ.get("REASONING_EFFORT", "off")  # off, high, max
MAX_AUDIT_WORKERS = int(os.environ.get("MAX_AUDIT_WORKERS", "50"))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-5.5"

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "sentinel-sops")

NEXUS_API_KEY = os.environ.get("NEXUS_API_KEY", "")
NEXUS_BASE_URL = os.environ.get("NEXUS_BASE_URL", "https://prod.nexus.pinecone.io")
NEXUS_CONTEXT_SLUG = os.environ.get("NEXUS_CONTEXT_SLUG", "sentinel-regs-test")

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

SNOWGLOBE_API_KEY = os.environ.get("SNOWGLOBE_API_KEY", "")

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")
JIRA_PROJECT_KEY = os.environ.get("JIRA_PROJECT_KEY", "")
JIRA_DEFAULT_ISSUE_TYPE = os.environ.get("JIRA_DEFAULT_ISSUE_TYPE", "Task")

LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY", "")
if LANGSMITH_API_KEY:
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "sentinel-agent")
    os.environ.setdefault("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-8B"
EMBEDDING_DIMENSION = 4096

PRICING = {
    "deepseek-ai/DeepSeek-V4-Pro": {"input": 1.75, "output": 3.50},
    "dedicated/deepseek-ai/DeepSeek-V3-0324-V7H70dy0RIqd": {"input": 2.00, "output": 6.00},
    "gpt-5.4-mini": {"input": 0.40, "output": 1.60},
    "gpt-5.5": {"input": 5.00, "output": 30.00},
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
