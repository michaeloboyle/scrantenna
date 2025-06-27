#!/usr/bin/env python3
"""
Generate knowledge graphs from news articles using GraphViz.
Creates Neo4j-style visual representations of entities and relationships.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set
import graphviz

# Try to load SpaCy model
spacy_available = False
nlp = None
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    spacy_available = True
    print("Using SpaCy for entity extraction")
except:
    print("SpaCy not available. Using fallback entity extraction.")

# Entity type mappings to Neo4j-style labels
ENTITY_TYPES = {
    "PERSON": {"label": "Person", "color": "#FF6B6B", "shape": "ellipse"},
    "ORG": {"label": "Organization", "color": "#4ECDC4", "shape": "box"},
    "GPE": {"label": "Location", "color": "#45B7D1", "shape": "diamond"},
    "EVENT": {"label": "Event", "color": "#96CEB4", "shape": "octagon"},
    "DATE": {"label": "Date", "color": "#FFEAA7", "shape": "circle"},
    "MONEY": {"label": "Money", "color": "#DDA0DD", "shape": "box"},
    "LAW": {"label": "Law", "color": "#F0A500", "shape": "box"}
}

# Relationship patterns for connecting entities
RELATIONSHIP_PATTERNS = [
    # PERSON-ORG relationships
    (r"(\w+(?:\s+\w+)*)\s+(?:of|from|at)\s+(\w+(?:\s+\w+)*)", "WORKS_AT"),
    (r"(\w+(?:\s+\w+)*)\s+(?:joined|joins)\s+(\w+(?:\s+\w+)*)", "JOINED"),
    (r"(\w+(?:\s+\w+)*)\s+(?:founded|started)\s+(\w+(?:\s+\w+)*)", "FOUNDED"),
    
    # PERSON-EVENT relationships
    (r"(\w+(?:\s+\w+)*)\s+(?:announced|reported|said)", "ANNOUNCED"),
    (r"(\w+(?:\s+\w+)*)\s+(?:was sentenced|sentenced)", "SENTENCED"),
    (r"(\w+(?:\s+\w+)*)\s+(?:cut|cuts)\s+(?:the\s+)?ribbon", "PARTICIPATED_IN"),
    
    # LOCATION-EVENT relationships
    (r"(?:in|at)\s+(\w+(?:\s+\w+)*)", "LOCATED_IN"),
    (r"filming\s+at\s+(\w+(?:\s+\w+)*)", "FILMED_AT"),
    
    # ORGANIZATION-EVENT relationships
    (r"(\w+(?:\s+\w+)*)\s+(?:issued|announced|reported)", "ISSUED"),
    (r"(\w+(?:\s+\w+)*)\s+(?:mailed|sent)", "SENT")
]

class NewsGraphGenerator:
    def __init__(self):
        self.entities = {}
        self.relationships = []
        self.entity_counter = 0
    
    def extract_entities(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract entities from text using SpaCy or fallback method."""
        if spacy_available and text:
            return self._extract_entities_spacy(text)
        else:
            return self._extract_entities_fallback(text)
    
    def _extract_entities_spacy(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract entities using SpaCy."""
        doc = nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in ENTITY_TYPES:
                clean_text = ent.text.strip()
                if len(clean_text) > 2:
                    entities.append((clean_text, ent.label_, ent.start_char))
        
        return entities
    
    def _extract_entities_fallback(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract entities using simple pattern matching."""
        if not text:
            return []
        
        entities = []
        words = text.split()
        
        # Extract proper nouns (capitalized words)
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w]', '', word)
            if len(clean_word) > 2 and clean_word[0].isupper():
                # Categorize by common patterns
                entity_type = "PERSON"  # Default
                
                # Location indicators
                if any(loc in clean_word.lower() for loc in ['scranton', 'pennsylvania', 'county', 'hall', 'theater', 'lake', 'road']):
                    entity_type = "GPE"
                # Organization indicators  
                elif any(org in clean_word.lower() for org in ['police', 'department', 'office', 'service', 'company', 'association', 'school']):
                    entity_type = "ORG"
                # Check if it's all caps (likely organization)
                elif clean_word.isupper() and len(clean_word) > 2:
                    entity_type = "ORG"
                
                entities.append((clean_word, entity_type, i))
        
        # Remove duplicates and return
        unique_entities = []
        seen = set()
        for entity in entities:
            if entity[0] not in seen:
                unique_entities.append(entity)
                seen.add(entity[0])
        
        return unique_entities[:10]  # Limit to 10 entities
    
    def extract_relationships(self, text: str, entities: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """Extract relationships between entities using pattern matching."""
        relationships = []
        
        for pattern, rel_type in RELATIONSHIP_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                subject = match.group(1).strip()
                if len(match.groups()) > 1:
                    obj = match.group(2).strip()
                else:
                    obj = "EVENT"  # Generic event object
                
                # Verify entities exist in our extracted entities
                subject_exists = any(subject.lower() in ent[0].lower() for ent in entities)
                obj_exists = any(obj.lower() in ent[0].lower() for ent in entities)
                
                if subject_exists or obj_exists:
                    relationships.append((subject, rel_type, obj))
        
        return relationships
    
    def add_entity(self, name: str, entity_type: str) -> str:
        """Add entity to graph and return unique ID."""
        clean_name = name.strip().title()
        entity_id = f"{entity_type}_{self.entity_counter}"
        
        if clean_name not in self.entities:
            self.entities[clean_name] = {
                "id": entity_id,
                "type": entity_type,
                "label": clean_name,
                "properties": ENTITY_TYPES.get(entity_type, ENTITY_TYPES["PERSON"])
            }
            self.entity_counter += 1
        
        return self.entities[clean_name]["id"]
    
    def add_relationship(self, subject: str, rel_type: str, obj: str):
        """Add relationship between entities."""
        self.relationships.append({
            "subject": subject,
            "relationship": rel_type,
            "object": obj
        })
    
    def process_article(self, article: Dict) -> Dict:
        """Process a single article and extract graph data."""
        # Combine title and description for analysis
        text = f"{article.get('title', '')} {article.get('description', '')}"
        
        # Extract entities
        entities = self.extract_entities(text)
        
        # Add entities to graph
        entity_ids = {}
        for ent_text, ent_type, position in entities:
            entity_id = self.add_entity(ent_text, ent_type)
            entity_ids[ent_text] = entity_id
        
        # Extract and add relationships
        relationships = self.extract_relationships(text, entities)
        for subj, rel, obj in relationships:
            if subj in entity_ids and obj in entity_ids:
                self.add_relationship(entity_ids[subj], rel, entity_ids[obj])
        
        return {
            "entities": len(entities),
            "relationships": len(relationships),
            "graph_data": {
                "nodes": list(entity_ids.values()),
                "edges": relationships
            }
        }
    
    def generate_graphviz(self, output_path: Path, title: str = "Scranton News Knowledge Graph"):
        """Generate GraphViz visualization of the knowledge graph."""
        dot = graphviz.Digraph(comment='News Knowledge Graph')
        dot.attr(rankdir='TB', size='12,8', dpi='300')
        dot.attr('node', fontname='Arial', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        # Add title
        dot.attr(label=title, fontsize='16', fontname='Arial Bold')
        
        # Add nodes (entities)
        for entity_name, entity_data in self.entities.items():
            props = entity_data["properties"]
            dot.node(
                entity_data["id"],
                label=entity_name,
                shape=props["shape"],
                style='filled',
                fillcolor=props["color"],
                fontcolor='white' if props["color"] in ['#FF6B6B', '#45B7D1'] else 'black'
            )
        
        # Add edges (relationships)
        for rel in self.relationships:
            dot.edge(
                rel["subject"],
                rel["object"],
                label=rel["relationship"].replace('_', ' '),
                color='gray'
            )
        
        # Save as both SVG and PNG
        dot.render(output_path.stem, directory=output_path.parent, format='svg', cleanup=True)
        dot.render(output_path.stem, directory=output_path.parent, format='png', cleanup=True)
        
        return str(output_path.parent / f"{output_path.stem}.svg")
    
    def generate_neo4j_cypher(self, output_path: Path):
        """Generate Neo4j Cypher queries for importing the graph."""
        cypher_queries = []
        
        # Create nodes
        cypher_queries.append("// Create entity nodes")
        for entity_name, entity_data in self.entities.items():
            entity_type = entity_data["type"]
            safe_name = entity_name.replace("'", "\\'")
            cypher_queries.append(
                f"CREATE (:{entity_type} {{id: '{entity_data['id']}', name: '{safe_name}'}})"
            )
        
        cypher_queries.append("\n// Create relationships")
        for rel in self.relationships:
            cypher_queries.append(
                f"MATCH (a), (b) WHERE a.id = '{rel['subject']}' AND b.id = '{rel['object']}' "
                f"CREATE (a)-[:{rel['relationship']}]->(b)"
            )
        
        # Save Cypher file
        with open(output_path, 'w') as f:
            f.write("\n".join(cypher_queries))
        
        return str(output_path)

def process_news_to_graph(news_file: Path, output_dir: Path):
    """Process news articles and generate knowledge graphs."""
    
    print(f"Loading news from: {news_file}")
    
    with open(news_file, 'r') as f:
        news_data = json.load(f)
    
    articles = news_data.get('articles', [])
    print(f"Found {len(articles)} articles")
    
    # Initialize graph generator
    graph_gen = NewsGraphGenerator()
    
    # Process each article
    total_entities = 0
    total_relationships = 0
    
    for i, article in enumerate(articles):
        print(f"Processing article {i+1}/{len(articles)}: {article.get('title', 'No title')[:50]}...")
        result = graph_gen.process_article(article)
        total_entities += result["entities"]
        total_relationships += result["relationships"]
    
    print(f"\\nExtracted {total_entities} entities and {total_relationships} relationships")
    print(f"Unique entities in graph: {len(graph_gen.entities)}")
    
    # Generate outputs
    output_dir.mkdir(exist_ok=True)
    
    # Generate GraphViz visualization
    svg_path = graph_gen.generate_graphviz(
        output_dir / "news_knowledge_graph",
        title=f"Scranton News Knowledge Graph ({datetime.now().strftime('%Y-%m-%d')})"
    )
    print(f"✓ GraphViz visualization: {svg_path}")
    
    # Generate Neo4j Cypher queries
    cypher_path = graph_gen.generate_neo4j_cypher(output_dir / "knowledge_graph.cypher")
    print(f"✓ Neo4j Cypher queries: {cypher_path}")
    
    # Save graph data as JSON
    graph_data = {
        "generated_at": datetime.now().isoformat(),
        "source_file": str(news_file),
        "total_entities": len(graph_gen.entities),
        "total_relationships": len(graph_gen.relationships),
        "entities": graph_gen.entities,
        "relationships": graph_gen.relationships
    }
    
    json_path = output_dir / "knowledge_graph.json"
    with open(json_path, 'w') as f:
        json.dump(graph_data, f, indent=2)
    print(f"✓ Graph data: {json_path}")
    
    return graph_data

def main():
    """Main function to generate knowledge graphs from news."""
    
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
    
    # Process news to graph
    output_dir = Path("../data/graph")
    graph_data = process_news_to_graph(latest_file, output_dir)
    
    print(f"\\n🎯 Knowledge graph generation complete!")
    print(f"📊 View visualization: {output_dir}/news_knowledge_graph.svg")
    print(f"🔍 Import to Neo4j: {output_dir}/knowledge_graph.cypher")

if __name__ == "__main__":
    main()