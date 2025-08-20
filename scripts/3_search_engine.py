"""
3_search_engine.py
==================

Core search functionality combining semantic and keyword-based search.

Key Dependencies:
- faiss-cpu
- sentence-transformers  
- pickle
- numpy

Summary:
This script implements the hybrid search engine that combines semantic similarity
(using FAISS + SentenceTransformers) with keyword matching. It includes specialized
logic for handling person names, departments, and health status queries.

Input: User natural language query
Output: Ranked list of relevant goals and milestones
"""

from src.keyword_scoring import calculate_keyword_score
from src.semantic_search import load_search_components, calculate_hybrid_score
import pickle
import faiss
from sentence_transformers import SentenceTransformer

def semantic_search_goals(query, index, metadata, model, k=50, min_score_threshold=0.1):
    """
    Perform semantic search on goals with hybrid scoring
    
    Args:
        query (str): Natural language query
        index: FAISS index
        metadata (list): Goal metadata
        model: SentenceTransformer model
        k (int): Number of results to retrieve
        min_score_threshold (float): Minimum score threshold
    
    Returns:
        tuple: (results, scores, needs_refinement, feedback)
    """
    try:
        # Generate embedding for the query
        query_embedding = model.encode([query])
        
        # Search using FAISS
        scores, indices = index.search(query_embedding.astype('float32'), k)
        
        # Get unique departments for better matching
        unique_departments = set()
        for item in metadata:
            dept = item.get('goal_department', '')
            if dept and str(dept).lower() != 'nan':
                unique_departments.add(dept)
        
        # SMART filtering approach
        results = []
        low_threshold_results = []
        
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(metadata):
                result = metadata[idx].copy()
                
                # Calculate semantic and keyword scores
                semantic_score = float(score)
                keyword_score = calculate_keyword_score(query, result, unique_departments)
                
                # Calculate hybrid score
                hybrid_score = calculate_hybrid_score(semantic_score, keyword_score, alpha=0.2)
                
                # Add scores to result
                result['semantic_score'] = semantic_score
                result['keyword_score'] = keyword_score
                result['hybrid_score'] = hybrid_score
                
                # Tiered filtering approach
                if hybrid_score >= min_score_threshold:
                    results.append(result)
                elif hybrid_score >= 0.05 and keyword_score >= 0.1:
                    low_threshold_results.append(result)
        
        # Combine and sort results
        all_results = results + low_threshold_results
        all_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        final_scores = [r['hybrid_score'] for r in all_results]
        needs_refinement = len(all_results) == 0
        feedback = "No results found" if needs_refinement else f"Found {len(all_results)} results"
        
        return all_results, final_scores, needs_refinement, feedback
        
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return [], [], True, f"Search error: {str(e)}"

def test_search_engine():
    """
    Test the search engine with sample queries
    """
    print("🔍 Testing Search Engine...")
    print("=" * 30)
    
    # Load search components
    index, metadata, model, stats = load_search_components()
    
    if not all([index, metadata, model]):
        print("❌ Could not load search components. Run build_index.py first.")
        return
    
    # Test queries
    test_queries = [
        "What goals are behind schedule?",
        "Show me engineering projects",
        "What is John working on?",
        "Which milestones are at risk?",
        "Revenue targets for this quarter"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results, scores, needs_refinement, feedback = semantic_search_goals(
            query, index, metadata, model, k=5
        )
        
        print(f"📊 {feedback}")
        
        if results:
            for i, result in enumerate(results[:3], 1):
                title = result.get('goal_title', 'N/A')
                owner = result.get('goal_owner', 'N/A')
                score = result.get('hybrid_score', 0)
                print(f"  {i}. {title} (Owner: {owner}) - Score: {score:.3f}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_search_engine()
