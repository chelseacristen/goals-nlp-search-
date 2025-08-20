"""
2_build_search_index.py
=======================

Build FAISS vector search index for goals and milestones data.

Key Dependencies:
- sentence-transformers
- faiss-cpu (or faiss-gpu)
- pickle
- numpy

Summary:
This script takes structured goals data and creates semantic embeddings using
SentenceTransformers. It builds a FAISS index for fast similarity search and
saves both the index and metadata for use in the search application.

Input: Structured goals data (from step 1)
Output: FAISS index, metadata pickle files, and index statistics
"""

import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

def create_searchable_text(goal_data):
    """
    Create comprehensive searchable text from goal data
    
    Args:
        goal_data (dict): Structured goal dictionary
    
    Returns:
        str: Combined searchable text
    """
    text_parts = []
    
    # Goal-level information
    text_parts.append(goal_data.get('goal_title', ''))
    text_parts.append(goal_data.get('goal_description', ''))
    text_parts.append(goal_data.get('goal_owner', ''))
    text_parts.append(goal_data.get('goal_department', ''))
    text_parts.append(goal_data.get('goal_health', ''))
    text_parts.append(goal_data.get('goal_key_initiative', ''))
    
    # Milestone information
    if goal_data.get('milestones'):
        for milestone in goal_data['milestones']:
            text_parts.append(milestone.get('title', ''))
            text_parts.append(milestone.get('description', ''))
            text_parts.append(milestone.get('owner', ''))
            text_parts.append(milestone.get('health', ''))
    
    # KPI information
    if goal_data.get('kpis'):
        for kpi in goal_data['kpis']:
            text_parts.append(kpi.get('title', ''))
            text_parts.append(kpi.get('description', ''))
    
    # Filter out empty strings and combine
    clean_text_parts = [str(part).strip() for part in text_parts if part and str(part).strip()]
    return ' '.join(clean_text_parts)

def build_search_index(structured_goals, model_name="all-MiniLM-L6-v2"):
    """
    Build FAISS search index from structured goals data
    
    Args:
        structured_goals (list): List of structured goal dictionaries
        model_name (str): SentenceTransformer model name
    
    Returns:
        tuple: (faiss_index, metadata, model, stats)
    """
    print(f"🤖 Loading SentenceTransformer model: {model_name}")
    model = SentenceTransformer(model_name)
    
    print("📝 Creating searchable text for each goal...")
    searchable_texts = []
    metadata = []
    
    for goal_data in structured_goals:
        searchable_text = create_searchable_text(goal_data)
        searchable_texts.append(searchable_text)
        metadata.append(goal_data)
    
    print(f"🔢 Generating embeddings for {len(searchable_texts)} goals...")
    embeddings = model.encode(searchable_texts, show_progress_bar=True)
    
    print("🏗️ Building FAISS index...")
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity
    index.add(embeddings.astype('float32'))
    
    # Calculate statistics
    stats = {
        'total_goals': len(structured_goals),
        'embedding_dimension': dimension,
        'model_name': model_name,
        'build_date': str(datetime.now()),
        'total_milestones': sum(len(goal.get('milestones', [])) for goal in structured_goals),
        'total_kpis': sum(len(goal.get('kpis', [])) for goal in structured_goals)
    }
    
    return index, metadata, model, stats

def save_search_components(index, metadata, stats, data_dir='data'):
    """
    Save all search components to disk
    
    Args:
        index: FAISS index
        metadata (list): Goal metadata
        stats (dict): Index statistics
        data_dir (str): Directory to save files
    """
    os.makedirs(data_dir, exist_ok=True)
    
    # Save FAISS index
    faiss.write_index(index, os.path.join(data_dir, 'goal_index.faiss'))
    print(f"✅ Saved FAISS index to {data_dir}/goal_index.faiss")
    
    # Save metadata
    with open(os.path.join(data_dir, 'goal_metadata.pkl'), 'wb') as f:
        pickle.dump(metadata, f)
    print(f"✅ Saved metadata to {data_dir}/goal_metadata.pkl")
    
    # Save statistics
    with open(os.path.join(data_dir, 'index_stats.pkl'), 'wb') as f:
        pickle.dump(stats, f)
    print(f"✅ Saved statistics to {data_dir}/index_stats.pkl")

if __name__ == "__main__":
    from datetime import datetime
    
    print("🚀 Building Goals Search Index...")
    print("=" * 40)
    
    # Load structured data from step 1
    print("📂 Loading structured goals data...")
    with open('data/structured_goals.pkl', 'rb') as f:
        structured_goals = pickle.load(f)
    
    print(f"📊 Found {len(structured_goals)} goals to index")
    
    # Build the search index
    index, metadata, model, stats = build_search_index(structured_goals)
    
    # Save all components
    save_search_components(index, metadata, stats)
    
    print(f"\n📈 Index Statistics:")
    print(f"- Total goals indexed: {stats['total_goals']}")
    print(f"- Total milestones: {stats['total_milestones']}")
    print(f"- Total KPIs: {stats['total_kpis']}")
    print(f"- Embedding dimension: {stats['embedding_dimension']}")
    print(f"- Model used: {stats['model_name']}")
    
    print("\n✅ Search index build complete!")
    print("Next step: Run 3_search_engine.py to test search functionality")
