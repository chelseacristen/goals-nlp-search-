"""
4_streamlit_app.py
==================

Streamlit web application for natural language goals search.

Key Dependencies:
- streamlit
- All dependencies from scripts 1-3
- requests (for LLM API calls)

Summary:
This script creates the user-facing web application that allows users to query
goals and milestones using natural language. It provides both search results
and AI-powered analysis modes.

Usage: streamlit run 4_streamlit_app.py

Features:
- Natural language query interface
- Semantic + keyword hybrid search
- AI-powered insights using RAG
- Interactive result display
"""

import streamlit as st
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from semantic_search import load_search_components, semantic_search_goals
from llm_integration import generate_rag_response, call_groq_llm

def display_goals_result(result, rank):
    """Display a single goals search result in Streamlit"""
    
    with st.expander(
        f"{rank}. {result['goal_title']}",
        expanded=(rank <= 3 and result.get('hybrid_score', 0) >= 0.3)
    ):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Goal:** {result['goal_title']}")
            if result.get('goal_description'):
                st.markdown(f"**Description:** {result['goal_description']}")
            if result.get('goal_last_update'):
                st.markdown(f"**Latest Update:** {result['goal_last_update']}")
        
        with col2:
            st.markdown(f"**Owner:** {result['goal_owner']}")
            st.markdown(f"**Department:** {result['goal_department']}")
            st.markdown(f"**Health:** {result['goal_health']}")
            if result.get('goal_end_date'):
                st.markdown(f"**End Date:** {result['goal_end_date']}")
        
        # Show milestones if they exist
        if result.get('milestones'):
            valid_milestones = [
                milestone for milestone in result['milestones'] 
                if milestone.get('title') and 
                str(milestone['title']).lower() not in ['nan', 'none', '']
            ]
            
            if valid_milestones:
                st.markdown("**Milestones:**")
                for milestone in valid_milestones:
                    st.markdown(f"• **{milestone['title']}**")
                    
                    if milestone.get('description') and str(milestone['description']).lower() not in ['nan', 'none', '']:
                        st.markdown(f"  _{milestone['description']}_")
                    
                    milestone_col1, milestone_col2 = st.columns(2)
                    with milestone_col1:
                        if milestone.get('owner') and str(milestone['owner']).lower() not in ['nan', 'none', '']:
                            st.markdown(f"  👤 {milestone['owner']}")
                        if milestone.get('health') and str(milestone['health']).lower() not in ['nan', 'none', '']:
                            st.markdown(f"  ❤️ {milestone['health']}")
                    with milestone_col2:
                        if milestone.get('end_date') and str(milestone['end_date']).lower() not in ['nan', 'none', '']:
                            st.markdown(f"  📅 {milestone['end_date']}")
                        if milestone.get('last_update'):
                            st.markdown(f"  💬 {milestone['last_update']}")

def create_goals_search_interface():
    """Create the main goals search interface"""
    st.header("🎯 Goals Natural Language Search")
    st.markdown("Ask questions about goals, milestones, and KPIs using natural language")
    
    # Load search components
    index, metadata, model, stats = load_search_components()
    
    if not all([index, metadata, model]):
        st.error("❌ Search components not found. Please run the build_index.py script first.")
        st.stop()
        return
    
    # Display index stats
    with st.sidebar:
        st.subheader("📊 Search Index Stats")
        if stats:
            st.metric("Total Goals", stats.get('total_goals', 'N/A'))
            st.metric("Total Milestones", stats.get('total_milestones', 'N/A'))
            st.metric("Total KPIs", stats.get('total_kpis', 'N/A'))
            st.text(f"Model: {stats.get('model_name', 'N/A')}")
        
        st.subheader("💡 Example Questions")
        st.markdown("""
        **Status & Analysis:**
        - "What's blocking our Q3 goals?"
        - "Which goals are at risk?"
        - "Show me delayed milestones"
        
        **People & Workload:**
        - "What is Sarah working on?"
        - "Who owns the most projects?"
        - "Show me engineering goals"
        
        **Health & Progress:**
        - "What goals are behind schedule?"
        - "Show me achieved milestones"
        - "Which departments need help?"
        """)
    
    # Main search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "What would you like to know about goals and milestones?",
            placeholder="e.g., 'What goals are behind schedule?', 'What is John working on?'",
            help="Ask questions in natural language"
        )
    
    with col2:
        response_mode = st.selectbox(
            "Response Mode:",
            ["🤖 AI Insights", "📋 Search Results"],
            help="AI Insights provides analysis, Search Results shows raw matches"
        )
    
    # Process query
    if query.strip():
        with st.spinner("🔍 Searching..."):
            results, scores, needs_refinement, feedback = semantic_search_goals(
                query, index, metadata, model, k=50, min_score_threshold=0.05
            )
        
        if response_mode == "🤖 AI Insights":
            # AI Analysis Mode
            if results:
                with st.spinner("🤖 Generating insights..."):
                    rag_response = generate_rag_response(query, results)
                
                st.subheader("🤖 AI Analysis")
                st.markdown(rag_response)
                
                with st.expander(f"📊 Source Data ({len(results)} goals analyzed)"):
                    st.info("The analysis above is based on these goals:")
                    for i, result in enumerate(results[:5], 1):
                        st.write(f"**{i}.** {result.get('goal_title', 'N/A')} (Owner: {result.get('goal_owner', 'N/A')})")
                    if len(results) > 5:
                        st.write(f"... and {len(results) - 5} more")
            else:
                st.error("❌ No relevant results found. Try rephrasing your question.")
        
        else:
            # Search Results Mode
            if results:
                st.subheader(f"🔍 Search Results ({len(results)} found)")
                for i, result in enumerate(results[:10], 1):  # Show top 10
                    display_goals_result(result, i)
            else:
                st.error("❌ No results found. Try a different search term.")

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Goals Natural Language Search",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Goals & Milestones Natural Language Search")
    st.markdown("---")
    
    # Check if search components exist
    if not os.path.exists('data/goal_index.faiss'):
        st.error("❌ Search index not found!")
        st.markdown("""
        **Setup Required:**
        1. Run `python scripts/1_data_preparation.py`
        2. Run `python scripts/2_build_search_index.py`
        3. Restart this application
        """)
        st.stop()
    
    # Create the search interface
    create_goals_search_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip:** Try different phrasings if you don't get the results you expect!")

if __name__ == "__main__":
    main()
