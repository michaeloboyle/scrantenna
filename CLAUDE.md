# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Scrantenna is a news analysis and knowledge graph project that collects news articles about Scranton, performs sentiment analysis, and builds knowledge graphs from the extracted information. The project also includes TimeSnapper activity log generation from screenshots.

## Common Development Commands

### Python Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install additional packages for Jupyter notebooks
pip install pytesseract pillow pandas vaderSentiment
```

### Running Jupyter Notebooks
```bash
# Start Jupyter notebook server
jupyter notebook

# Run specific notebooks programmatically
jupyter nbconvert --execute notebooks/ingest_news.ipynb
jupyter nbconvert --execute notebooks/sentiment_analysis.ipynb
jupyter nbconvert --execute notebooks/build_knowledge_graph.ipynb
```

### Data Processing Pipeline
```bash
# Manual execution order for data processing
# 1. Ingest news data (requires API key)
# 2. Perform sentiment analysis
# 3. Build knowledge graphs
# 4. Generate activity logs from screenshots (optional)
```

## Project Architecture

### Data Flow Pipeline
1. **News Ingestion** (`ingest_news.ipynb`): Fetches articles from NewsAPI about Scranton
2. **Sentiment Analysis** (`sentiment_analysis.ipynb`): Uses VADER sentiment analyzer 
3. **Knowledge Graph Building** (`build_knowledge_graph.ipynb`): Extracts entities and events using SpaCy NLP
4. **Activity Logging** (`activity_log_generator.ipynb`): OCR analysis of TimeSnapper screenshots

### Directory Structure
- `notebooks/` - Jupyter notebooks for data processing pipeline
- `data/raw/` - Raw news articles in JSON format
- `data/sentiment/` - Sentiment analysis results per article
- `data/graph/` - Generated Cypher queries and GraphViz DOT files
- `models/` - Model configurations (currently empty)
- `2024-09-10/` - TimeSnapper screenshots for activity analysis

### Key Technologies
- **SpaCy** - NLP processing for entity extraction (requires `en_core_web_sm` model)
- **NetworkX** - Graph data structures and algorithms
- **Neo4j** - Graph database with Cypher query generation
- **VADER Sentiment** - Sentiment analysis of news content
- **PyTesseract** - OCR for screenshot text extraction
- **BeautifulSoup** - Web scraping utilities
- **Papermill** - Programmatic notebook execution

### Entity Recognition and Graph Schema
- **Persons** (Q5) - Extracted PERSON entities from articles
- **Organizations** (Q43229) - Extracted ORG entities 
- **Locations** (Q515) - Extracted GPE (geopolitical entities)
- **Events** (Q1656682) - Detected events with timestamps and locations
- Relationships: Events OCCURRED_AT locations

### API Configuration
The project uses NewsAPI with a configured API key for fetching Scranton-related news articles. The API key is currently hardcoded in `ingest_news.ipynb` and should be moved to environment variables for security.

### Screenshot Analysis
TimeSnapper screenshots are processed to identify:
- ChatGPT discussions
- Web searches
- Email activity  
- Code editing sessions
- Timestamps and activity classification