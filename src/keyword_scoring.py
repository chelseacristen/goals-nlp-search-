# src/keyword_scoring.py
"""
Keyword-based scoring logic for goals search
"""

def calculate_keyword_score(query, result, all_departments=None):
    """Calculate keyword matching score with improved logic for person name matching and health status weighting"""
    query_words = set(query.lower().split())
    
    # Helper function to safely get text (handle NaN/None values)
    def safe_text(value):
        if value is None or (isinstance(value, float) and str(value).lower() == 'nan'):
            return ''
        return str(value)
    
    # Enhanced ownership query detection
    ownership_keywords = {'own', 'owns', 'owner', 'owned', 'owning', 'responsible', 'assigned', 'managing', 'lead', 'leads', 'belong', 'belongs'}
    has_ownership_query = bool(query_words & ownership_keywords)
    
    # Health status keywords for better matching
    health_keywords = {
        'behind': ['behind', 'delayed', 'late', 'overdue'],
        'at risk': ['risk', 'risky', 'at-risk', 'atrisk', 'concern', 'concerning', 'yellow'],
        'on track': ['track', 'on-track', 'ontrack', 'good', 'green', 'progress', 'progressing'],
        'exceeded': ['exceeded', 'exceeding', 'ahead', 'early', 'beating'],
        'achieved': ['achieved', 'completed', 'done', 'finished', 'complete'],
        'not started': ['not-started', 'notstarted', 'waiting', 'pending', 'queue'],
        'not tracked': ['not-tracked', 'nottracked', 'untracked', 'unknown']
    }
    
    # Create reverse mapping for quick lookup
    keyword_to_health = {}
    for health_status, keywords in health_keywords.items():
        for keyword in keywords:
            keyword_to_health[keyword] = health_status
    
    has_health_query = bool(query_words & set(keyword_to_health.keys()))
    
    # Collect all text from the result
    all_text = []
    goal_title = safe_text(result.get('goal_title', ''))
    all_text.append(goal_title)
    all_text.append(safe_text(result.get('goal_description', '')))
    all_text.append(safe_text(result.get('goal_department', '')))
    all_text.append(safe_text(result.get('goal_owner', '')))
    all_text.append(safe_text(result.get('goal_health', '')))
    
    # Add milestone text
    if result.get('milestones'):
        for milestone in result['milestones']:
            all_text.append(safe_text(milestone.get('title', '')))
            all_text.append(safe_text(milestone.get('description', '')))
            all_text.append(safe_text(milestone.get('owner', '')))
    
    # Add KPI text  
    if result.get('kpis'):
        for kpi in result['kpis']:
            all_text.append(safe_text(kpi.get('title', '')))
            all_text.append(safe_text(kpi.get('description', '')))
    
    # Combine all text and tokenize
    combined_text = ' '.join([text for text in all_text if text.strip()]).lower()
    doc_words = set(combined_text.split())
    
    # Calculate basic coverage
    intersection = query_words & doc_words
    query_word_coverage = len(intersection) / len(query_words) if query_words else 0
    
    # Enhanced scoring logic for names, departments, health status...
    # [Include the full logic from your original function]
    
    return min(1.0, query_word_coverage)  # Simplified for demo
