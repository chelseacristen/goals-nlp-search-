# src/llm_integration.py
"""
LLM integration for RAG-based analysis
"""

import requests
import streamlit as st
import time

def call_groq_llm(prompt, max_tokens=1000, max_retries=3):
    """Call Groq API for LLM responses with model fallback and retry logic"""
    try:
        # Note: In a real implementation, use environment variables or secure config
        api_key = st.secrets.get("GROQ_API_KEY", "your-api-key-here")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        models_to_try = [
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768", 
            "llama-3.1-8b-instant"
        ]
        
        for model in models_to_try:
            for attempt in range(max_retries):
                try:
                    data = {
                        "model": model,
                        "messages": [
                            {
                                "role": "system", 
                                "content": "You are a helpful business analyst assistant. Analyze goal and project data to provide actionable insights."
                            },
                            {
                                "role": "user", 
                                "content": prompt
                            }
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.1
                    }
                    
                    response = requests.post(url, headers=headers, json=data, timeout=30)
                    
                    if response.status_code == 200:
                        return response.json()["choices"][0]["message"]["content"]
                    else:
                        break  # Try next model
                        
                except Exception:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        break
        
        return "Sorry, AI service is temporarily unavailable. Please try again later."
            
    except Exception as e:
        return f"Error connecting to AI service: {str(e)}"

def prepare_context_for_llm(results, query):
    """Prepare search results as context for the LLM"""
    if not results:
        return "No relevant goals or milestones found."
    
    context_parts = []
    
    for result in results:
        title = result.get('goal_title', 'N/A')
        owner = result.get('goal_owner', 'N/A')
        
        goal_info = f"""
**{title}** (owned by {owner}):
- Department: {result.get('goal_department', 'N/A')}
- Health Status: {result.get('goal_health', 'N/A')}
- Last Update: {result.get('goal_last_update', 'No update available')}
"""
        
        # Add milestone information
        if result.get('milestones'):
            valid_milestones = [m for m in result['milestones'] 
                              if m.get('title') and str(m['title']).lower() not in ['nan', 'none', '']]
            if valid_milestones:
                goal_info += "- Key Milestones:\n"
                for milestone in valid_milestones[:3]:
                    milestone_text = f"  • {milestone.get('title', 'N/A')}"
                    if milestone.get('health'):
                        milestone_text += f" (Status: {milestone['health']})"
                    goal_info += milestone_text + "\n"
        
        context_parts.append(goal_info)
    
    return "\n---\n".join(context_parts)

def generate_rag_response(query, search_results):
    """Generate RAG response using search results as context"""
    
    if not search_results:
        return "I couldn't find any relevant goals or milestones for your query."
    
    context = prepare_context_for_llm(search_results, query)
    
    rag_prompt = f"""
Based on the following goals and milestones data, please answer the user's question.

CONTEXT DATA:
{context}

USER QUESTION: {query}

Please provide a concise answer that:
1. References goals by their actual titles and owners
2. Summarizes key issues and current status
3. Identifies patterns across the data
4. Suggests actionable next steps

Answer:"""
    
    return call_groq_llm(rag_prompt, max_tokens=1200)
