# src/semantic_search.py
"""
Semantic search utilities and FAISS operations
"""

import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

def load_search_components(data_dir='data'):
    """Load FAISS index, metadata, and model for goals search"""
    try:
        # Load FAISS index
        index = faiss.read_index(os.path.join(data_dir, 'goal_index.faiss'))
        
        # Load metadata
        with open(os.path.join(data_dir, 'goal_metadata.pkl'), 'rb') as f:
            metadata = pickle.load(f)
        
        # Load sentence transformer model
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Load stats if available
        stats = {}
        try:
            with open(os.path.join(data_dir, 'index_stats.pkl'), 'rb') as f:
                stats = pickle.load(f)
        except FileNotFoundError:
            pass
        
        return index, metadata, model, stats
    
    except FileNotFoundError as e:
        print(f"Could not find search files: {e}")
        return None, None, None, {}

def calculate_hybrid_score(semantic_score, keyword_score, alpha=0.2):
    """
    Combine semantic and keyword scores
    alpha: weight for semantic score (0.2 = 20% semantic, 80% keyword)
    """
    return alpha * semantic_score + (1 - alpha) * keyword_score
