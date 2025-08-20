# Goals NLP Search Scipts #
Respository containing scripts on how to query structured goals data using natural language.

## 1: Data Preparation and Anonymization (1_data_preparation.py): ##
Data preparation pipeline that loads raw Cascade goals/milestone exports, performs data quality validation, structures hierarchical goal-milestone-KPI relationships, and generates anonymized sample datasets for demonstration purposes. The script handles date standardization, creates nested data structures for complex goal hierarchies, and ensures data integrity through validation reporting.

*Dependencies: pandas, numpy, faker
Data Sources: Cascade goals exports, milestone data, KPI tracking files*

## 2: Semantic Search Index Builder (2_build_search_index.py): ##
FAISS-based vector search index construction that creates searchable text from hierarchical goals data, generates semantic embeddings using SentenceTransformers, and builds optimized similarity search indices with cosine distance metrics. The script includes text preparation that preserves goal-milestone-KPI relationships, implements quality feedback systems for search validation, and provides robust testing frameworks for query optimization.

*Dependencies: sentence-transformers, faiss-cpu, pickle, numpy
Data Sources: Structured goals data from step 1*

## 3: Hybrid Search Engine Core (3_search_engine.py): ##
Natural language search engine that combines semantic similarity scoring with intelligent keyword matching, featuring specialized logic for person name recognition, department queries, and health status classification. The script implements multi-tier relevance filtering, provides search result ranking, and includes query understanding for ownership patterns and project status inquiries.
*Dependencies: faiss-cpu, sentence-transformers, custom scoring modules
Data Sources: FAISS indices and metadata from step 2*

## 4: Interactive Web Application (4_streamlit_app.py): ##
Production-ready Streamlit web application providing natural language querying interface for goals and milestones data, featuring dual-mode operation with raw search results and AI-powered RAG analysis. The application includes responsive UI design, real-time search feedback, contextual help systems, and integration with external LLM services for intelligent business insights generation.

*Dependencies: streamlit, requests, all previous script dependencies
Data Sources: Search indices, LLM API integration (Groq)*
