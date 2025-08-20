# Goals Natural Language Search # 
A natural language search engine for goals and milestones data, combining semantic search with keyword matching and AI-powered analysis.
Features

🔍 Hybrid Search: Combines semantic similarity with keyword matching
🤖 AI Analysis: RAG-powered insights and recommendations
👥 Person-Aware: Handles queries about specific people and ownership
📊 Status-Aware: Understands health status and project state queries
🎯 Interactive Web UI: Streamlit-based interface for easy querying

## Quick Start ##
1. Installation
bashgit clone https://github.com/yourusername/goals-nlp-search.git
cd goals-nlp-search
pip install -r requirements.txt

2. Prepare Your Data
bash# Place your Cascade export in data/sample_goals.csv
python scripts/1_data_preparation.py

3. Build Search Index
bashpython scripts/2_build_search_index.py

5. Run the Application
bashstreamlit run scripts/4_streamlit_app.py

6. Test Search Engine (Optional)
bashpython scripts/3_search_engine.py
Data Format
Input CSV Structure

## Your goals CSV should include these columns: ##

goal_title: Title of the goal
goal_description: Detailed description
goal_owner: Person responsible
goal_department: Department/team
goal_health: Status (On Track, At Risk, Behind, etc.)
goal_end_date: Target completion date
goal_last_update: Latest status update

Milestone Data (Optional)

milestone_title: Milestone name
milestone_description: Details
milestone_owner: Responsible person
milestone_health: Status
milestone_end_date: Due date
milestone_last_update: Latest update

## Configuration ##
API Keys
Create a Streamlit secrets file or environment variables:
toml# .streamlit/secrets.toml
GROQ_API_KEY = "your-groq-api-key-here"
Search Parameters
Edit config/config.py to adjust:

Search result thresholds
Hybrid scoring weights
Model selection

## Example Queries ##
Status & Analysis

"What goals are behind schedule?"
"Which milestones are at risk?"
"Show me delayed engineering projects"

*People & Workload*

"What is Sarah working on?"
"Who owns the most at-risk projects?"
"Show me John's Q4 priorities"

*Insights & Patterns*

"What patterns do you see in our delays?"
"Which departments need help?"
"Summarize our goal progress"

## Technical Architecture ##
Search Pipeline

## Query Processing:##  Parse natural language input
## Semantic Search:## Generate embeddings and search FAISS index
## Keyword Matching:## Score based on exact keyword matches
## Hybrid Scoring:## Combine semantic + keyword scores
## AI Analysis:## Use RAG to generate insights (optional)

## Key Components##

## FAISS Index:## Fast semantic similarity search
## SentenceTransformers:## Text embedding generation
## Hybrid Scoring:## Balances semantic + keyword relevance
## RAG Integration:## LLM-powered analysis and insights

## Dependencies##
Core Requirements
streamlit>=1.28.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
pandas>=1.5.0
numpy>=1.21.0
requests>=2.28.0
Optional (for data generation)
faker>=19.0.0

## Troubleshooting ##
Common Issues

"Search components not found": Run the build_index.py script first
"No results found": Try rephrasing your query or check data quality
"AI service unavailable": Check your Groq API key configuration

Performance Tips

Index builds are one-time operations (cache results)
Larger k values in search may improve recall but slow performance
Adjust scoring thresholds based on your data characteristics

Contributing

Fork the repository
Create a feature branch
Add tests for new functionality
Submit a pull request


File Structure
goals-nlp-search/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── data/                       
│   ├── sample_goals.csv        # Sample/anonymized data
│   └── README.md               # Data documentation
├── scripts/                    
│   ├── 1_data_preparation.py   # Clean and structure data
│   ├── 2_build_search_index.py # Create FAISS index
│   ├── 3_search_engine.py      # Test search functionality
│   └── 4_streamlit_app.py      # Web application
├── src/                        
│   ├── __init__.py            
│   ├── keyword_scoring.py      # Keyword matching logic
│   ├── semantic_search.py      # FAISS operations
│   └── llm_integration.py      # RAG and LLM calls
└── config/
    └── config.py               # Configuration settings
