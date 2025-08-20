config/config.py
"""
Configuration settings for goals search engine
"""
Search Parameters
DEFAULT_SEARCH_THRESHOLD = 0.05
DEFAULT_SEARCH_K = 50
HYBRID_SCORE_ALPHA = 0.2  # Weight for semantic vs keyword scoring
Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MAX_RESULTS_DISPLAY = 20
LLM Configuration
MAX_TOKENS = 1200
LLM_TEMPERATURE = 0.1
MAX_RETRIES = 3
Data Paths
DATA_DIR = "data"
INDEX_FILE = "goal_index.faiss"
METADATA_FILE = "goal_metadata.pkl"
STATS_FILE = "index_stats.pkl"
