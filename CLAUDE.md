# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Scrantenna is a news analysis and knowledge graph project that collects news articles about Scranton, performs sentiment analysis, and builds knowledge graphs from the extracted information. The project features a TikTok-style "Shorts" viewer for consuming news in an engaging visual format, with intelligent text distillation powered by LLM technology.

## Common Development Commands

### Python Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install additional packages for Jupyter notebooks
pip install pytesseract pillow pandas vaderSentiment

# For LLM-powered distillation (optional but recommended)
pip install openai
export OPENAI_API_KEY=your_api_key_here
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

### News Shorts Viewer
```bash
# Generate and view TikTok-style news shorts
cd shorts/
python3 generate_shorts.py          # Generate shorts data with distillation
./launch_shorts.sh                  # Start local server
# Open http://localhost:8000

# Navigation:
# - Arrow keys ↑↓ or swipe up/down to navigate
# - Spacebar to advance
# - 't' key or horizontal swipe to toggle Original/Distilled formats
```

### Data Processing Pipeline
```bash
# Manual execution order for data processing
# 1. Ingest news data with distillation (requires API key)
# 2. Perform sentiment analysis
# 3. Build knowledge graphs
# 4. Generate shorts for visual consumption
# 5. Generate activity logs from screenshots (optional)
```

## Project Architecture

### Data Flow Pipeline
1. **News Ingestion** (`ingest_news.ipynb`): Fetches articles from NewsAPI about Scranton with intelligent LLM-based distillation
2. **Shorts Generation** (`shorts/generate_shorts.py`): Creates TikTok-style visual news consumption format
3. **Sentiment Analysis** (`sentiment_analysis.ipynb`): Uses VADER sentiment analyzer 
4. **Knowledge Graph Building** (`build_knowledge_graph.ipynb`): Extracts entities and events using SpaCy NLP
5. **Activity Logging** (`activity_log_generator.ipynb`): OCR analysis of TimeSnapper screenshots

### Directory Structure
- `notebooks/` - Jupyter notebooks for data processing pipeline
- `shorts/` - TikTok-style news viewer with animated typography and distillation
- `data/daily/` - Daily news articles with original and distilled versions
- `data/sentiment/` - Sentiment analysis results per article
- `data/graph/` - Generated Cypher queries and GraphViz DOT files
- `models/` - Model configurations (currently empty)
- `2024-09-10/` - TimeSnapper screenshots for activity analysis

### Key Technologies
- **OpenAI GPT** - Intelligent text distillation for shorts (optional, falls back to rule-based)
- **HTML5/CSS3/JavaScript** - Full-screen animated shorts viewer with touch gestures
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

For LLM-powered text distillation, set `OPENAI_API_KEY` environment variable. The system gracefully falls back to rule-based distillation if OpenAI is unavailable.

### Shorts Viewer Features
- **Full-screen animated typography** with gradient backgrounds that act as "palette cleansers"
- **Triple view modes**: Text (original/distilled) and Knowledge Graph visualization
- **Interactive knowledge graphs** showing entities and relationships in Neo4j-style format
- **Mobile-responsive** with touch gestures and swipe navigation
- **Auto-advance** (10 seconds per short) with manual navigation controls
- **Efficient caching** to avoid redundant API calls and processing

### Graph Visualization
```bash
# Generate knowledge graphs from news articles
cd shorts/
python3 graph_generator.py          # Creates GraphViz and Neo4j outputs

# Controls in shorts viewer:
# - 't' key: Toggle Original/Distilled text formats
# - 'g' key: Toggle between Text and Graph views
# - Arrow keys: Navigate between shorts
```

## Distribution & Monetization Strategy

### Content Distribution Platforms
- **TikTok**: Export shorts as video files for native platform distribution
- **Instagram Reels**: Adapt format for Instagram's vertical video requirements
- **YouTube Shorts**: Leverage YouTube's monetization and discovery algorithms
- **Twitter/X**: Share as video threads with link-backs to full articles
- **LinkedIn**: Professional news content for business audience
- **Local Facebook Groups**: Targeted distribution to Scranton community groups

### Video Export Pipeline
```bash
# Future implementation: Convert HTML shorts to video
# Using headless browser automation + screen recording
cd shorts/
python3 export_videos.py --platform tiktok     # 9:16 aspect ratio, 60 FPS
python3 export_videos.py --platform youtube    # Optimized for YouTube Shorts
python3 export_videos.py --platform instagram  # Instagram Reels specifications
```

### Monetization Opportunities
- **Local Business Sponsorships**: Sponsored content in news shorts about Scranton businesses
- **Real Estate Integration**: Property highlights within relevant local news
- **Event Promotion**: Paid promotion of local events, festivals, and activities
- **Educational Content**: Sponsored "distilled" explanations of local government processes
- **Affiliate Marketing**: Local service recommendations with affiliate partnerships
- **Premium Features**: Ad-free experience, extended shorts, custom topics
- **API Licensing**: Sell distillation and shorts generation technology to other local news organizations

### Community Engagement Features
- **User-Generated Content**: Allow community submission of local news tips
- **Interactive Polls**: Engagement features within shorts (opinion polling on local issues)
- **Live Events**: Real-time shorts during city council meetings, local events
- **Personalization**: AI-driven content curation based on user interests and location

### Screenshot Analysis
TimeSnapper screenshots are processed to identify:
- ChatGPT discussions
- Web searches
- Email activity  
- Code editing sessions
- Timestamps and activity classification