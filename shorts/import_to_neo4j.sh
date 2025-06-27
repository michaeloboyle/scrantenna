#!/bin/bash
# Scrantenna Neo4j Import Script
# Generated on 2025-06-26T16:56:17.262077

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
