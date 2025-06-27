#!/usr/bin/env python3
"""
Generate optimized shorts data from news articles.
Creates condensed, visual-friendly versions for the shorts player.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Try to import OpenAI for LLM-based distillation
try:
    import openai
    llm_available = True
    client = openai.OpenAI()
except ImportError:
    print("OpenAI not available. Falling back to simple distillation.")
    llm_available = False
    client = None

def clean_text(text: str, truncate: bool = False) -> str:
    """Clean text for shorts display."""
    if not text:
        return ""
    
    # Remove character count indicators
    text = re.sub(r'\[\+\d+ chars\]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Only truncate if explicitly requested AND not already distilled
    # Distilled content should never be truncated
    if truncate and len(text) > 200 and not is_distilled_content(text):
        text = text[:197] + "..."
    
    return text

def is_distilled_content(text: str) -> bool:
    """Check if text appears to be already distilled (short, direct statements)."""
    if not text:
        return True
    
    # Distilled content characteristics:
    # - Usually under 100 characters
    # - Direct subject-verb-object format
    # - No article references
    return (len(text) < 100 or 
            not any(phrase in text.lower() for phrase in ['the article', 'the story', 'according to']))

def create_distilled_version_llm(text: str) -> str:
    """Create intelligent distilled version using LLM."""
    if not llm_available or not text:
        return ""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Extract the core facts from news text into direct, precise statements. Use simple subject-verb-object format. Avoid referring to 'the article' or 'the story'. State facts directly as if reporting them yourself. Keep it under 80 characters. Be specific about WHO did WHAT."
                },
                {
                    "role": "user", 
                    "content": f"Distill this news text: {text}"
                }
            ],
            max_tokens=30,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM distillation failed: {e}")
        return create_distilled_version_fallback(text)

def create_distilled_version_fallback(text: str) -> str:
    """Fallback distillation using simple text processing."""
    if not text:
        return ""
    
    # Extract first sentence
    sentences = text.split('.')
    first_sentence = sentences[0].strip() if sentences else text
    
    # Remove common article references and clean up
    first_sentence = re.sub(r'\(.*?\)', '', first_sentence)  # Remove parentheses
    first_sentence = re.sub(r'^(The|A|An)\s+', '', first_sentence)  # Remove articles
    
    # Don't truncate fallback distillation - keep it natural length
    if not first_sentence.endswith('.'):
        first_sentence += "."
    
    return first_sentence

def create_distilled_version(text: str) -> str:
    """Create distilled version using best available method."""
    if llm_available:
        return create_distilled_version_llm(text)
    else:
        return create_distilled_version_fallback(text)

def extract_simple_entities(text: str) -> List[Dict]:
    """Extract meaningful entities with focus on people, places, organizations, and events."""
    if not text:
        return []
    
    entities = []
    
    # Extract quoted works/titles like 'Final Act', "The Office"
    quoted_works = re.findall(r'[\'"]([A-Z][A-Za-z\s]{2,25})[\'"]', text)
    for work in quoted_works:
        work = work.strip()
        if len(work.split()) <= 5 and work not in ['s', 'The', 'A', 'An', 'Of', 'In', 'On']:
            entities.append({"name": work, "type": "Work"})
    
    # Extract person names - more precise patterns
    person_patterns = [
        r'\b([A-Z][a-z]{2,15}\s[A-Z][a-z]{2,15})\b',  # First Last
        r'\b([A-Z][a-z]{2,15}\s[A-Z]\.\s[A-Z][a-z]{2,15})\b',  # First M. Last
        r'\b(Mayor\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b',  # Mayor Name
        r'\b(Judge\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b',  # Judge Name
        r'\b(Commissioner\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b',  # Commissioner Name
    ]
    
    for pattern in person_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Clean up titles
            clean_name = re.sub(r'^(Mayor|Judge|Commissioner)\s+', '', match)
            if (len(clean_name.split()) >= 1 and 
                not any(word.lower() in ['said', 'says', 'announced', 'reported'] for word in clean_name.split()) and
                not any(e['name'] == clean_name for e in entities)):
                entities.append({"name": clean_name, "type": "Person"})
    
    # Extract specific locations with better patterns
    location_patterns = [
        r'\b(Scranton)\b',
        r'\b(Pennsylvania)\b',
        r'\b(Lackawanna\s+County)\b',
        r'\b([A-Z][a-z]+\s+(?:County|City|Township|Borough))\b',
        r'\b([A-Z][a-z]+\s+(?:Theater|Theatre|Hall|Hospital|School|University|Field|Lake|Road|Street|Avenue))\b',
        r'\b(City\s+Hall)\b',
        r'\b(Ritz\s+Theater)\b',
        r'\b(Weston\s+Field)\b',
        r'\b(Harveys\s+Lake)\b',
    ]
    
    for pattern in location_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if not any(e['name'].lower() == match.lower() for e in entities):
                entities.append({"name": match, "type": "Location"})
    
    # Extract organizations with better precision
    org_patterns = [
        r'\b((?:[A-Z][a-z]+\s+)*(?:Police|Department|Office|Service|Company|Association|Corp|Inc|LLC))\b',
        r'\b((?:University\s+of\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College))\b',
        r'\b([A-Z]{3,6})\b',  # Acronyms like FBI, CNN, NWS
        r'\b(Dunder-Mifflin\s+Paper\s+Company)\b',
        r'\b(National\s+Weather\s+Service)\b',
    ]
    
    for pattern in org_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if (len(match) > 2 and 
                match not in ['THE', 'AND', 'FOR', 'WITH', 'FROM', 'BUT', 'NOT'] and
                not any(e['name'] == match for e in entities)):
                entities.append({"name": match, "type": "Organization"})
    
    # Extract events and activities
    event_patterns = [
        r'\b(Pride\s+Month)\b',
        r'\b(Flash\s+Flood\s+Warning)\b',
        r'\b([A-Z][a-z]+\s+(?:Game|Tournament|Festival|Event|Summit))\b',
    ]
    
    for pattern in event_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if not any(e['name'].lower() == match.lower() for e in entities):
                entities.append({"name": match, "type": "Event"})
    
    # Always include Scranton as a location if not present
    if not any(e['name'].lower() == 'scranton' for e in entities):
        entities.append({"name": "Scranton", "type": "Location"})
    
    # Filter out noise and ensure quality
    quality_entities = []
    for entity in entities:
        name = entity['name'].strip()
        if (len(name) > 2 and 
            not re.match(r'^(To|In|On|At|By|As|Of|Up|Or|If|It|Is|Be|Do|Go|He|We|My|So|No|An|Am|Us|Me|The|And|For|With|From)$', name, re.IGNORECASE) and
            len(name.split()) <= 4):  # Reasonable entity length
            quality_entities.append(entity)
    
    return quality_entities[:10]  # Allow up to 10 quality entities

def extract_simple_relationships(text: str, entities: List[Dict]) -> List[Dict]:
    """Extract meaningful relationships between entities."""
    relationships = []
    
    # Create entity lookup for easier matching
    entity_names = [e['name'] for e in entities]
    entity_dict = {e['name']: e for e in entities}
    
    # Comprehensive relationship patterns
    relationship_patterns = [
        # People and roles
        (r'\b(Mayor|Judge|Commissioner)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'HAS_ROLE'),
        
        # Location relationships
        (r'\b(\w+(?:\s+\w+)*)\s+(?:in|at|of)\s+(Scranton|Pennsylvania|Lackawanna\s+County)', 'LOCATED_IN'),
        (r'\b(filming|located|situated|based)\s+(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'LOCATED_AT'),
        
        # Work relationships
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:joined|stars\s+in|appears\s+in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'WORKS_ON'),
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:plays|portrays)\s+', 'ACTS_IN'),
        
        # Organizational relationships
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:from|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Police|Department|Office|Company)))', 'MEMBER_OF'),
        
        # Event relationships
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:announced|issued|declared)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'ANNOUNCED'),
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:sentenced|charged)\s+', 'LEGAL_ACTION'),
        
        # Temporal relationships
        (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:during|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'OCCURRED_DURING'),
    ]
    
    for pattern, rel_type in relationship_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match.groups()) >= 2:
                subject_name = match.group(1).strip()
                object_name = match.group(2).strip()
                
                # Find matching entities (partial matches allowed)
                subject_entity = None
                object_entity = None
                
                for entity in entities:
                    if subject_name.lower() in entity['name'].lower() or entity['name'].lower() in subject_name.lower():
                        subject_entity = entity
                    if object_name.lower() in entity['name'].lower() or entity['name'].lower() in object_name.lower():
                        object_entity = entity
                
                if subject_entity and object_entity and subject_entity['name'] != object_entity['name']:
                    relationships.append({
                        "from": subject_entity['name'], 
                        "to": object_entity['name'], 
                        "type": rel_type
                    })
    
    # Add standard geographic relationships
    for entity in entities:
        if entity['type'] == 'Location' and entity['name'] != 'Scranton':
            if 'scranton' in entity['name'].lower():
                continue  # Don't create self-relationships
            
            # Connect locations to Scranton
            scranton_entity = next((e for e in entities if e['name'] == 'Scranton'), None)
            if scranton_entity:
                relationships.append({
                    "from": entity['name'],
                    "to": "Scranton",
                    "type": "NEAR"
                })
    
    # Add organizational relationships
    for entity in entities:
        if entity['type'] == 'Organization':
            scranton_entity = next((e for e in entities if e['name'] == 'Scranton'), None)
            if scranton_entity and 'scranton' in text.lower():
                relationships.append({
                    "from": entity['name'],
                    "to": "Scranton",
                    "type": "OPERATES_IN"
                })
    
    # Remove duplicates
    unique_relationships = []
    seen = set()
    for rel in relationships:
        key = (rel['from'], rel['to'], rel['type'])
        if key not in seen:
            seen.add(key)
            unique_relationships.append(rel)
    
    return unique_relationships[:8]  # Limit relationships for readability

def generate_article_graph(article: Dict, index: int) -> Dict:
    """Generate graph data for a single article using free LLM extraction."""
    try:
        # Try to use free LLM extractor first
        from free_llm_extractor import create_free_llm_graph_data
        return create_free_llm_graph_data(article, index)
    except ImportError:
        print("Free LLM extractor not available, falling back to simple extraction")
        # Fallback to simple extraction
        text = f"{article.get('title', '')} {article.get('description', '')}"
        entities = extract_simple_entities(text)
        relationships = extract_simple_relationships(text, entities)
        
        return {
            "entities": entities,
            "relationships": relationships,
            "svg": generate_svg_graph(entities, relationships, index)
        }

def generate_svg_graph(entities: List[Dict], relationships: List[Dict], index: int) -> str:
    """Generate SVG representation of the graph."""
    if not entities:
        return '<svg width="300" height="200"><text x="150" y="100" text-anchor="middle" fill="white">No entities found</text></svg>'
    
    colors = {
        'Person': '#FF6B6B',
        'Organization': '#4ECDC4', 
        'Location': '#45B7D1',
        'Work': '#9C27B0',
        'Event': '#FF9800'
    }
    
    svg = '<svg width="300" height="200" viewBox="0 0 300 200" class="graph-svg">'
    
    # Draw entities as circles
    for i, entity in enumerate(entities):
        x = 50 + (i % 3) * 100
        y = 50 + (i // 3) * 60
        color = colors.get(entity['type'], '#888')
        
        svg += f'<circle cx="{x}" cy="{y}" r="20" fill="{color}" stroke="white" stroke-width="2"/>'
        svg += f'<text x="{x}" y="{y-25}" text-anchor="middle" fill="white" font-size="10" font-weight="bold">{entity["name"][:8]}</text>'
        svg += f'<text x="{x}" y="{y+35}" text-anchor="middle" fill="white" font-size="8">{entity["type"]}</text>'
    
    # Draw relationships as lines
    for rel in relationships:
        from_entity = next((e for e in entities if e['name'] == rel['from']), None)
        to_entity = next((e for e in entities if e['name'] == rel['to']), None)
        
        if from_entity and to_entity:
            from_index = entities.index(from_entity)
            to_index = entities.index(to_entity)
            
            x1 = 50 + (from_index % 3) * 100
            y1 = 50 + (from_index // 3) * 60
            x2 = 50 + (to_index % 3) * 100
            y2 = 50 + (to_index // 3) * 60
            
            svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="1" opacity="0.7"/>'
            
            # Add relationship label
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            svg += f'<text x="{mid_x}" y="{mid_y}" text-anchor="middle" fill="white" font-size="8">{rel["type"]}</text>'
    
    svg += '</svg>'
    return svg

def create_short_from_article(article: Dict, index: int) -> Dict:
    """Convert a news article into a short format."""
    
    # Extract key information - never truncate distilled content
    title = clean_text(article.get('title', ''), truncate=True)
    title_distilled = clean_text(article.get('title_distilled', ''))  # Never truncate distilled
    description = clean_text(article.get('description', ''), truncate=True)
    description_distilled = clean_text(article.get('description_distilled', ''))  # Never truncate distilled
    
    # Use description as content since API content is truncated
    content = description
    content_distilled = clean_text(article.get('content_distilled', ''))  # Never truncate distilled
    
    # Generate intelligent distilled versions if not already present
    if not title_distilled and title:
        title_distilled = create_distilled_version(title)
    
    if not content_distilled and content:
        content_distilled = create_distilled_version(content)
    
    # Generate inline graph data for this article
    graph_data = generate_article_graph(article, index)
    
    short = {
        "id": f"short_{index}",
        "title": title,
        "title_distilled": title_distilled,
        "description": description,
        "description_distilled": description_distilled,
        "content": content,
        "content_distilled": content_distilled,
        "graph": graph_data,
        "source": article.get('source', {}).get('name', 'Unknown'),
        "publishedAt": article.get('publishedAt', ''),
        "url": article.get('url', ''),
        "urlToImage": article.get('urlToImage', ''),
        "duration": 10000,  # 10 seconds per short
        "background_gradient": get_background_gradient(index),
        "animation_delay": min(index * 0.1, 1.0)  # Stagger animations
    }
    
    return short

def get_background_gradient(index: int) -> str:
    """Get a background gradient based on index."""
    gradients = [
        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
        "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
        "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
        "linear-gradient(135deg, #ff8a80 0%, #ea80fc 100%)",
        "linear-gradient(135deg, #82b1ff 0%, #b388ff 100%)",
        "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)"
    ]
    return gradients[index % len(gradients)]

def generate_shorts_from_news(news_file: Path, max_shorts: int = 15) -> Dict:
    """Generate shorts data from news file."""
    
    print(f"Loading news from: {news_file}")
    
    with open(news_file, 'r') as f:
        news_data = json.load(f)
    
    articles = news_data.get('articles', [])
    print(f"Found {len(articles)} articles")
    
    # Check if we already have LLM-distilled versions
    has_llm_distilled = news_data.get('distillation_method') == 'llm'
    if has_llm_distilled:
        print("✓ Using existing LLM-distilled versions from news data")
    elif llm_available:
        print("🤖 Generating new LLM-distilled versions")
    else:
        print("📝 Using fallback distillation")
    
    # Filter and sort articles for best shorts
    # Prioritize articles with both title and description
    good_articles = []
    for article in articles[:max_shorts]:
        if (article.get('title') and 
            article.get('description') and 
            len(article.get('title', '')) > 10):
            good_articles.append(article)
    
    print(f"Selected {len(good_articles)} articles for shorts")
    
    # Generate shorts
    shorts = []
    for i, article in enumerate(good_articles):
        short = create_short_from_article(article, i)
        shorts.append(short)
    
    # Create shorts data structure
    shorts_data = {
        "generated_at": datetime.now().isoformat(),
        "source_file": str(news_file),
        "total_shorts": len(shorts),
        "total_duration": len(shorts) * 8,  # seconds
        "has_svo": news_data.get('has_svo', False),
        "shorts": shorts
    }
    
    return shorts_data

def check_if_shorts_current(news_file: Path) -> bool:
    """Check if shorts data is current with the news file."""
    shorts_file = Path("shorts_data.json")
    
    if not shorts_file.exists():
        return False
    
    try:
        with open(shorts_file, 'r') as f:
            shorts_data = json.load(f)
        
        # Check if source file matches and is recent
        source_file = shorts_data.get('source_file', '')
        if str(news_file) in source_file:
            # Check if generated recently (within last hour)
            generated_at = shorts_data.get('generated_at', '')
            if generated_at:
                from datetime import datetime, timedelta
                gen_time = datetime.fromisoformat(generated_at)
                if datetime.now() - gen_time < timedelta(hours=1):
                    return True
        
        return False
    except:
        return False

def main():
    """Main function to generate shorts."""
    import sys
    
    # Check for force flag
    force_regenerate = '--force' in sys.argv
    
    # Find the latest news file
    data_dir = Path("../data/daily")
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return
    
    news_files = sorted(data_dir.glob("scranton_news_*.json"), reverse=True)
    if not news_files:
        print("No news files found")
        return
    
    latest_file = news_files[0]
    
    # Check if shorts are already current (unless forced)
    if not force_regenerate and check_if_shorts_current(latest_file):
        print(f"✓ Shorts data is current for {latest_file.name}")
        print("🔄 Use --force to regenerate anyway")
        return
    
    # Generate shorts data
    shorts_data = generate_shorts_from_news(latest_file)
    
    # Save shorts data
    output_file = Path("shorts_data.json")
    with open(output_file, 'w') as f:
        json.dump(shorts_data, f, indent=2)
    
    print(f"Generated {shorts_data['total_shorts']} shorts")
    print(f"Total duration: {shorts_data['total_duration']} seconds")
    print(f"Saved to: {output_file}")
    
    # Generate a simple player launcher
    create_player_launcher()

def create_player_launcher():
    """Create a simple launcher script."""
    launcher_content = '''#!/bin/bash
# Scrantenna Shorts Player Launcher

echo "🎬 Starting Scrantenna Shorts..."
echo "📱 Full-screen news stories with SVO toggle"
echo ""

# Check if we have a local server running
if command -v python3 &> /dev/null; then
    echo "🚀 Starting local server on port 8000..."
    echo "📱 Open: http://localhost:8000"
    echo "⌨️  Controls: ↑↓ arrows, spacebar, 't' to toggle format"
    echo ""
    python3 -m http.server 8000
else
    echo "❌ Python3 not found. Please install Python to run the server."
    echo "💡 Or open index.html directly in your browser"
fi
'''
    
    with open("launch_shorts.sh", 'w') as f:
        f.write(launcher_content)
    
    # Make executable
    os.chmod("launch_shorts.sh", 0o755)
    print("Created launcher: ./launch_shorts.sh")

if __name__ == "__main__":
    main()