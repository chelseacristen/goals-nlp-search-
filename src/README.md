# Supporting Modules: #

## Keyword Scoring Engine (src/keyword_scoring.py): ##
Keyword matching algorithm with domain-specific logic for business goal queries, implementing person name detection, department recognition, health status mapping, and ownership query enhancement. Features text processing for handling possessive forms, abbreviations, and business terminology common in project management contexts.

*Dependencies: pandas, numpy, re (standard library)
Data Sources: Goal metadata dictionaries, department lists, predefined name/keyword mappings*

## Semantic Search Utilities (src/semantic_search.py): ##
Core semantic search infrastructure providing FAISS index management, embedding model loading, hybrid score calculation, and search component caching. Implements efficient similarity search with configurable parameters and robust error handling for production deployment.

*Dependencies: faiss-cpu, sentence-transformers, pickle, numpy, os (standard library)
Data Sources: FAISS index files (.faiss), pickled metadata (.pkl), SentenceTransformer model cache* 

## LLM Integration Module (src/llm_integration.py): ##
Retrieval-Augmented Generation (RAG) system with context preparation, multi-model fallback strategies, and robust API error handling. Features natural language response generation using search results as context, with comprehensive retry logic and graceful degradation for service reliability.

*Dependencies: requests, streamlit, time (standard library), json (standard library)
Data Sources: Groq API endpoints, search result metadata, API key configuration (secrets.toml)*
