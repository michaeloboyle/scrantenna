#!/usr/bin/env python3
"""
Neo4j Export Utility for Scrantenna
Converts processed news data into Neo4j Cypher format for advanced graph analysis.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Set, Tuple
from pathlib import Path


class ScrantennaNeo4jExporter:
    """Export Scrantenna data to Neo4j Cypher format."""
    
    def __init__(self):
        self.entities: Set[Tuple[str, str]] = set()  # (name, type)
        self.relationships: List[Dict] = []
        self.articles: List[Dict] = []
        self.cypher_commands: List[str] = []
    
    def load_shorts_data(self, shorts_file: str = "shorts_data.json") -> bool:
        """Load data from shorts JSON file."""
        try:
            with open(shorts_file, 'r') as f:
                data = json.load(f)
            
            self.articles = data.get('shorts', [])
            print(f"✓ Loaded {len(self.articles)} articles from {shorts_file}")
            return True
            
        except FileNotFoundError:
            print(f"❌ File not found: {shorts_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return False
    
    def extract_graph_data(self):
        """Extract entities and relationships from articles."""
        print("📊 Extracting graph data...")
        
        for article in self.articles:
            # Extract entities
            entities = article.get('graph', {}).get('entities', [])
            for entity in entities:
                name = entity.get('name', '').strip()
                entity_type = entity.get('type', 'UNKNOWN')
                
                if name and len(name) > 1:
                    self.entities.add((name, entity_type))
            
            # Extract relationships
            relationships = article.get('graph', {}).get('relationships', [])
            for rel in relationships:
                if all(key in rel for key in ['from', 'to', 'type']):
                    self.relationships.append({
                        'from': rel['from'],
                        'to': rel['to'],
                        'type': rel['type'],
                        'article_id': article.get('id', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source': article.get('source', 'Unknown')
                    })
        
        print(f"✓ Found {len(self.entities)} unique entities")
        print(f"✓ Found {len(self.relationships)} relationships")
    
    def generate_cypher_commands(self):
        """Generate Cypher commands for Neo4j import."""
        self.cypher_commands = []
        
        # Add cleanup and constraints
        self._add_setup_commands()
        
        # Create entity nodes
        self._create_entity_nodes()
        
        # Create article nodes
        self._create_article_nodes()
        
        # Create relationships
        self._create_relationships()
        
        # Add indices and constraints
        self._add_indices()
        
        print(f"✓ Generated {len(self.cypher_commands)} Cypher commands")
    
    def _add_setup_commands(self):
        """Add database setup commands."""
        self.cypher_commands.extend([
            "// Scrantenna Knowledge Graph Import",
            f"// Generated on {datetime.now().isoformat()}",
            "",
            "// Clear existing data (CAUTION: This will delete all data!)",
            "// MATCH (n) DETACH DELETE n;",
            "",
            "// Create constraints (run these first)",
            "CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;",
            "CREATE CONSTRAINT article_id IF NOT EXISTS FOR (a:Article) REQUIRE a.id IS UNIQUE;",
            ""
        ])
    
    def _create_entity_nodes(self):
        """Create Cypher commands for entity nodes."""
        self.cypher_commands.append("// Create Entity Nodes")
        
        # Group entities by type for better organization
        entities_by_type = {}
        for name, entity_type in self.entities:
            if entity_type not in entities_by_type:
                entities_by_type[entity_type] = []
            entities_by_type[entity_type].append(name)
        
        for entity_type, names in entities_by_type.items():
            self.cypher_commands.append(f"// {entity_type} entities")
            
            for name in sorted(names):
                # Escape single quotes in names
                safe_name = name.replace("'", "\\'")
                
                cypher = (f"MERGE (e:Entity:{entity_type} {{name: '{safe_name}'}}) "
                         f"SET e.type = '{entity_type}', e.created_at = datetime();")
                
                self.cypher_commands.append(cypher)
            
            self.cypher_commands.append("")
    
    def _create_article_nodes(self):
        """Create Cypher commands for article nodes."""
        self.cypher_commands.append("// Create Article Nodes")
        
        for article in self.articles:
            article_id = article.get('id', '')
            title = article.get('title', '').replace("'", "\\'")
            source = article.get('source', 'Unknown').replace("'", "\\'")
            published_at = article.get('publishedAt', '')
            url = article.get('url', '').replace("'", "\\'")
            
            cypher = (f"CREATE (a:Article {{id: '{article_id}', "
                     f"title: '{title}', "
                     f"source: '{source}', "
                     f"published_at: '{published_at}', "
                     f"url: '{url}'}});")
            
            self.cypher_commands.append(cypher)
        
        self.cypher_commands.append("")
    
    def _create_relationships(self):
        """Create Cypher commands for relationships."""
        self.cypher_commands.append("// Create Relationships")
        
        # Group relationships by type
        relationships_by_type = {}
        for rel in self.relationships:
            rel_type = rel['type']
            if rel_type not in relationships_by_type:
                relationships_by_type[rel_type] = []
            relationships_by_type[rel_type].append(rel)
        
        for rel_type, rels in relationships_by_type.items():
            self.cypher_commands.append(f"// {rel_type} relationships")
            
            for rel in rels:
                from_name = rel['from'].replace("'", "\\'")
                to_name = rel['to'].replace("'", "\\'")
                article_id = rel.get('article_id', '')
                source = rel.get('source', '').replace("'", "\\'")
                
                cypher = (f"MATCH (from:Entity {{name: '{from_name}'}}), "
                         f"(to:Entity {{name: '{to_name}'}}) "
                         f"CREATE (from)-[r:{rel_type} {{article_id: '{article_id}', "
                         f"source: '{source}'}}]->(to);")
                
                self.cypher_commands.append(cypher)
            
            self.cypher_commands.append("")
        
        # Create article-entity relationships
        self.cypher_commands.append("// Article-Entity relationships")
        for article in self.articles:
            article_id = article.get('id', '')
            entities = article.get('graph', {}).get('entities', [])
            
            for entity in entities:
                entity_name = entity.get('name', '').replace("'", "\\'")
                confidence = entity.get('confidence', 0.5)
                
                cypher = (f"MATCH (a:Article {{id: '{article_id}'}}), "
                         f"(e:Entity {{name: '{entity_name}'}}) "
                         f"CREATE (a)-[:MENTIONS {{confidence: {confidence}}}]->(e);")
                
                self.cypher_commands.append(cypher)
        
        self.cypher_commands.append("")
    
    def _add_indices(self):
        """Add performance indices."""
        self.cypher_commands.extend([
            "// Create Indices for Performance",
            "CREATE INDEX entity_type_idx IF NOT EXISTS FOR (e:Entity) ON (e.type);",
            "CREATE INDEX article_source_idx IF NOT EXISTS FOR (a:Article) ON (a.source);",
            "CREATE INDEX article_published_idx IF NOT EXISTS FOR (a:Article) ON (a.published_at);",
            ""
        ])
    
    def export_to_file(self, output_file: str = "scrantenna_graph.cypher"):
        """Export Cypher commands to file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.cypher_commands))
            
            print(f"✅ Exported to {output_file}")
            print(f"📊 Import Statistics:")
            print(f"   • Entities: {len(self.entities)}")
            print(f"   • Articles: {len(self.articles)}")
            print(f"   • Relationships: {len(self.relationships)}")
            print(f"   • Cypher commands: {len(self.cypher_commands)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def generate_sample_queries(self, output_file: str = "sample_queries.cypher"):
        """Generate useful sample queries for analysis."""
        
        sample_queries = [
            "// Scrantenna Sample Neo4j Queries",
            f"// Generated on {datetime.now().isoformat()}",
            "",
            "// 1. Find most mentioned entities",
            "MATCH (e:Entity)<-[:MENTIONS]-(a:Article)",
            "RETURN e.name, e.type, COUNT(a) as mentions",
            "ORDER BY mentions DESC",
            "LIMIT 10;",
            "",
            "// 2. Find entities connected to Scranton",
            "MATCH (scranton:Entity {name: 'Scranton'})-[r]-(connected)",
            "RETURN scranton.name, type(r), connected.name, connected.type;",
            "",
            "// 3. Articles by source with entity counts",
            "MATCH (a:Article)-[:MENTIONS]->(e:Entity)",
            "RETURN a.source, COUNT(DISTINCT e) as entity_count, COUNT(a) as articles",
            "ORDER BY entity_count DESC;",
            "",
            "// 4. Find relationship paths between entities",
            "MATCH path = (from:Entity)-[*1..3]-(to:Entity)",
            "WHERE from.name = 'Paige Cognetti' AND to.name = 'Scranton'",
            "RETURN path",
            "LIMIT 5;",
            "",
            "// 5. Timeline analysis - entities by publication date",
            "MATCH (a:Article)-[:MENTIONS]->(e:Entity)",
            "WHERE a.published_at IS NOT NULL",
            "RETURN date(a.published_at) as date, COUNT(DISTINCT e) as entities",
            "ORDER BY date DESC;",
            "",
            "// 6. Find most influential entities (highest degree centrality)",
            "MATCH (e:Entity)",
            "RETURN e.name, e.type, size((e)--()) as connections",
            "ORDER BY connections DESC",
            "LIMIT 10;",
            "",
            "// 7. Community detection (requires APOC or GDS library)",
            "// CALL gds.louvain.stream('entityGraph')",
            "// YIELD nodeId, communityId",
            "// RETURN gds.util.asNode(nodeId).name as entity, communityId",
            "// ORDER BY communityId;",
            "",
            "// 8. Find articles mentioning multiple entity types",
            "MATCH (a:Article)-[:MENTIONS]->(e:Entity)",
            "WITH a, COLLECT(DISTINCT e.type) as types",
            "WHERE size(types) > 2",
            "RETURN a.title, a.source, types",
            "ORDER BY size(types) DESC;",
            "",
            "// 9. Recent news analysis (last 7 days)",
            "MATCH (a:Article)-[:MENTIONS]->(e:Entity)",
            "WHERE a.published_at >= date() - duration('P7D')",
            "RETURN e.name, e.type, COUNT(a) as recent_mentions",
            "ORDER BY recent_mentions DESC",
            "LIMIT 15;",
            "",
            "// 10. Entity co-occurrence analysis",
            "MATCH (a:Article)-[:MENTIONS]->(e1:Entity),",
            "      (a)-[:MENTIONS]->(e2:Entity)",
            "WHERE e1.name < e2.name",
            "RETURN e1.name, e2.name, COUNT(a) as co_occurrences",
            "ORDER BY co_occurrences DESC",
            "LIMIT 20;"
        ]
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sample_queries))
            
            print(f"✅ Sample queries exported to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Sample queries export failed: {e}")
            return False
    
    def create_import_script(self, script_file: str = "import_to_neo4j.sh"):
        """Create a shell script for easy Neo4j import."""
        
        script_content = f"""#!/bin/bash
# Scrantenna Neo4j Import Script
# Generated on {datetime.now().isoformat()}

echo "🔄 Starting Scrantenna graph import to Neo4j..."

# Configuration
NEO4J_URI="neo4j://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"
CYPHER_FILE="scrantenna_graph.cypher"

# Check if Neo4j is running
echo "🔍 Checking Neo4j connection..."
if ! nc -z localhost 7687; then
    echo "❌ Neo4j is not running on port 7687"
    echo "   Start Neo4j Desktop or run: neo4j start"
    exit 1
fi

# Check if cypher file exists
if [ ! -f "$CYPHER_FILE" ]; then
    echo "❌ Cypher file not found: $CYPHER_FILE"
    echo "   Run: python neo4j_export.py"
    exit 1
fi

# Import data using cypher-shell
echo "📊 Importing data to Neo4j..."
cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" -f "$CYPHER_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Import completed successfully!"
    echo "🌐 Open Neo4j Browser: http://localhost:7474"
    echo "📊 Run sample queries from: sample_queries.cypher"
else
    echo "❌ Import failed"
    exit 1
fi
"""
        
        try:
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            # Make script executable
            os.chmod(script_file, 0o755)
            
            print(f"✅ Import script created: {script_file}")
            print(f"   Run with: ./{script_file}")
            return True
            
        except Exception as e:
            print(f"❌ Script creation failed: {e}")
            return False


def main():
    """Main export function."""
    print("🚀 Scrantenna Neo4j Exporter")
    print("=" * 40)
    
    exporter = ScrantennaNeo4jExporter()
    
    # Load data
    if not exporter.load_shorts_data():
        return False
    
    # Extract graph data
    exporter.extract_graph_data()
    
    # Generate Cypher commands
    exporter.generate_cypher_commands()
    
    # Export to files
    success = True
    success &= exporter.export_to_file()
    success &= exporter.generate_sample_queries()
    success &= exporter.create_import_script()
    
    if success:
        print("\n🎉 Export completed successfully!")
        print("\nNext steps:")
        print("1. Start Neo4j Desktop or server")
        print("2. Run: ./import_to_neo4j.sh")
        print("3. Open Neo4j Browser: http://localhost:7474")
        print("4. Try queries from sample_queries.cypher")
    else:
        print("\n❌ Export failed")
    
    return success


if __name__ == "__main__":
    main()